# -*- coding: utf-8 -*-
"""Build D16 geometry. Run: blender --background --python scripts/curiosity_d16_blender.py"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]/'03_Cabinets/CB001_Curiosity_Low_Maple_Walnut'
OUT=ROOT/'models/D16';OUT.mkdir(parents=True,exist_ok=True)
p=json.loads((OUT/'parameters.json').read_text())
p.update(depth=370.,door_projection=34.66,door_thickness=32.,door_rear_clearance=2.66,door_width=330.,door_height=1110.,door_bottom=310.,door_x=[10.,345.],meeting_gap=5.,closed_depth=404.66)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
p.update(leg_section=40.,leg_x=[5.,640.],leg_y=[19.062534625,299.062534625],leg_front_setback=19.062534625,leg_rear_setback=30.937465375)
p.update(post=30.,post_x=30.,post_y=40.)
parts=[]
metal=bpy.data.materials.new('Antique brass - reference appearance');metal.diffuse_color=(.23,.15,.055,1);metal.use_nodes=True
mb=metal.node_tree.nodes.get('Principled BSDF');mb.inputs['Base Color'].default_value=(.23,.15,.055,1);mb.inputs['Metallic'].default_value=.82;mb.inputs['Roughness'].default_value=.32
def wood(name,color):
    mat=bpy.data.materials.new(name);mat.diffuse_color=(*color,1);mat.use_nodes=True
    n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.43
    tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=3;tex.inputs['Detail'].default_value=2
    coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(35,35,2)
    l.new(coord.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[1].position=.82
    ramp.color_ramp.elements[0].color=(*(v*.8 for v in color),1);ramp.color_ramp.elements[1].color=(*(min(1,v*1.15) for v in color),1)
    l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
    return mat
walnut=wood('Walnut - illustrative matte',(.065,.027,.012))
maple=wood('Maple - illustrative matte',(.48,.32,.16))
glass=bpy.data.materials.new('Reeded glass - 4mm assumed');glass.diffuse_color=(.8,.92,.96,.18);glass.use_nodes=True
bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.93,.98,1,1)
bs.inputs['Transmission Weight'].default_value=1;bs.inputs['Roughness'].default_value=.055;bs.inputs['IOR'].default_value=1.5
collection=bpy.data.collections.new('CABINET_D09_GEOMETRY');bpy.context.scene.collection.children.link(collection)
def addmesh(name,verts,faces,mat,record=True):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata([[v/1000 for v in a] for a in verts],[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);collection.objects.link(obj);obj.data.materials.append(mat)
    if record:parts.append({'name':name,'material':'METAL' if mat==metal else ('GLASS' if mat==glass else ('MAPLE' if mat==maple else 'WALNUT')),'vertices_mm':verts,'faces':faces})
    return obj
def box(name,x,y,z,w,d,h,mat):
    assert min(w,d,h)>0,name
    verts=[[x,y,z],[x+w,y,z],[x+w,y+d,z],[x,y+d,z],[x,y,z+h],[x+w,y,z+h],[x+w,y+d,z+h],[x,y+d,z+h]]
    obj=addmesh(name,verts,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]],mat)
    mod=obj.modifiers.new('0.4 mm edge easing - render only','BEVEL');mod.width=.0004;mod.segments=2
    obj.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return obj
W,H,D,P=p['width'],p['height'],p['depth'],p['post'];R=p['rail'];B=p['maple_bead'];F=p['door_walnut'];g=p['perimeter_gap']
PX=30.;PY=40.
Z0=p['leg_height']+R;Z1=H-R
# Four solid upright posts, lower exposed portion constructed as walnut borders and maple core.
for ix,x in enumerate([0,W-PX]):
    for iy,y in enumerate([0,D-PY]):
        key=f'POST_{ix}{iy}'
        box(key+'_upper',x,y,300,PX,PY,H-R-300,walnut)
        lx=p['leg_x'][ix];ly=p['leg_y'][iy];L=p['leg_section'];E=p['leg_edge']
        box(key+'_shoe',lx,ly,0,L,L,22,walnut)
        box(key+'_core',lx+E,ly+E,22,L-2*E,L-2*E,278,maple)
        for aa in [0,L-E]:
            for bb in [0,L-E]:box(key+f'_corner_{aa}_{bb}',lx+aa,ly+bb,22,E,E,278,walnut)
        for aa in [0,L-E]:box(key+f'_maple_x{aa}',lx+aa,ly+E,22,E,L-2*E,278,maple)
        for bb in [0,L-E]:box(key+f'_maple_y{bb}',lx+E,ly+bb,22,L-2*E,E,278,maple)
# Lower body frame and floor, four top border members.
for z in [300,H-R]:
    for y in [0,D-R]:box(f'RAIL_FB_{z}_{y}',PX if z==300 else 0,y,z,W-2*PX if z==300 else W,R,R,walnut)
    for x in [0,W-R]:box(f'RAIL_SIDE_{z}_{x}',x,PY if z==300 else R,z,R,D-2*PY if z==300 else D-2*R,R,walnut)
# D16 bottom fix: close the 30mm strips between the old P-offset panel and R-width rails.
# Notch the four post footprints; triangulate the concave cap for CAD/GLB/viewer consistency.
from mathutils.geometry import tessellate_polygon
outline=[(PX,R),(W-PX,R),(W-PX,PY),(W-R,PY),(W-R,D-PY),(W-PX,D-PY),
         (W-PX,D-R),(PX,D-R),(PX,D-PY),(R,D-PY),(R,PY),(PX,PY)]
flat=[Vector((x,y,0)) for x,y in outline]
def cross2(a,b,c):return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x)
remaining=list(range(len(flat)));cap=[]
while len(remaining)>3:
    for k,b in enumerate(remaining):
        a=remaining[k-1];c=remaining[(k+1)%len(remaining)]
        if cross2(flat[a],flat[b],flat[c])<=0:continue
        if any(all(cross2(flat[u],flat[v],flat[q])>=0 for u,v in [(a,b),(b,c),(c,a)]) for q in remaining if q not in (a,b,c)):continue
        cap.append([a,b,c]);remaining.pop(k);break
    else:raise ValueError('Cannot triangulate floor')
cap.append(remaining)
index={tuple(v):i for i,v in enumerate(flat)};n=len(outline)
verts=[[x,y,z] for z in [305,325] for x,y in outline]
faces=[]
for tri in cap:
    ids=[v if isinstance(v,int) else index[tuple(v)] for v in tri]
    if (flat[ids[1]]-flat[ids[0]]).cross(flat[ids[2]]-flat[ids[0]]).z < 0:
        ids.reverse()
    faces.extend([list(reversed(ids)),[i+n for i in ids]])
for i in range(n):
    j=(i+1)%n;faces.append([i,j,j+n,i+n])
addmesh('Cabinet floor - continuous notched panel',verts,faces,maple)
for x,w in [(R,W/2-12.5-R),(W/2+12.5,W/2-12.5-R)]:box(f'TOP_maple_{x}',x,R,H-R,w,D-2*R,R,maple)
box('TOP_centre_walnut',W/2-12.5,R,H-R,25,D-2*R,R,walnut)
for z in p['stretcher_levels']:
    for x in [p['leg_x'][0],p['leg_x'][1]+p['leg_section']-25]:box(f'SIDE_stretcher_{x}_{z}',x,p['leg_y'][0]+p['leg_section'],z,25,p['leg_y'][1]-p['leg_y'][0]-p['leg_section'],22,walnut)
# D16: one front and one rear stretcher, midway between side stretchers.
for label,y in [('FRONT',p['leg_y'][0]),('REAR',p['leg_y'][1]+p['leg_section']-25)]:
    box(f'ADDED_{label}_stretcher',p['leg_x'][0]+p['leg_section'],y,sum(p['stretcher_levels'])/len(p['stretcher_levels']),p['leg_x'][1]-p['leg_x'][0]-p['leg_section'],25,22,walnut)
for z in p['shelf_levels']:box(f'SHELF_{z}',PX,PY,z,W-2*PX,D-2*PY,p['shelf_thickness'],maple)
# Back is an explicit provisional board, not inferred from the appearance image.
box('BACK_8mm_ASSUMED',PX,D-20,Z0,W-2*PX,8,Z1-Z0,maple)

def front_ring(name,x,y,z,w,h,t,depth,mat):
    box(name+'_L',x,y,z,t,depth,h,mat);box(name+'_R',x+w-t,y,z,t,depth,h,mat)
    box(name+'_B',x+t,y,z,w-2*t,depth,t,mat);box(name+'_T',x+t,y,z+h-t,w-2*t,depth,t,mat)
def reeded(name,origin,w,h,side=False):
    # Geometrically modelled sinusoidal ribs, 6mm pitch, 0.6mm relief.
    n=math.ceil(w/1.0);v=[]
    for i in range(n+1):
        u=w*i/n;relief=.3*(1+math.cos(2*math.pi*u/6))
        for dep,z in [(0,0),(0,h),(4+relief,0),(4+relief,h)]:
            a=(dep,u,z) if side else (u,dep,z)
            v.append([origin[j]+a[j] for j in range(3)])
    f=[]
    for i in range(n):
        a=4*i;b=4*(i+1)
        f.extend([[a,b,b+1,a+1],[a+2,a+3,b+3,b+2],[a,a+2,b+2,b],[a+1,b+1,b+3,a+3]])
    f.extend([[0,1,3,2],[4*n,4*n+2,4*n+3,4*n+1]])
    if side:f=[list(reversed(face)) for face in f]
    addmesh(name,v,f,glass)
dw=p['door_width'];dz=p['door_bottom'];dh=p['door_height'];door_y=-p['door_projection']
for i,x in enumerate(p['door_x']):
    front_ring(f'DOOR{i}_walnut',x,door_y,dz,dw,dh,F,p['door_thickness'],walnut)
    front_ring(f'DOOR{i}_maple9',x+F,door_y+3,dz+F,dw-2*F,dh-2*F,B,12,maple)
    reeded(f'DOOR{i}_GLASS',[x+F+B,door_y+10,dz+F+B],dw-2*(F+B),dh-2*(F+B))
    # Original DXF front/side extents x5: oval 24x39, projection35, centres324/361 at z865.
    hx=324. if i==0 else 361.
    def metal_part(name,centre,radii):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24)
        tmp=bpy.context.object
        vv=[[centre[k]+v.co[k]*radii[k] for k in range(3)] for v in tmp.data.vertices]
        ff=[list(f.vertices) for f in tmp.data.polygons]
        bpy.data.objects.remove(tmp,do_unlink=True)
        ob=addmesh(name,vv,ff,metal)
        for poly in ob.data.polygons:poly.use_smooth=True
    metal_part(f'HANDLE{i}_oval',(hx,door_y-23,865),(12,12,19.5))
    metal_part(f'HANDLE{i}_neck_ASSUMED',(hx,door_y-7,865),(3.5,7,3.5))
    metal_part(f'HANDLE{i}_base_ASSUMED',(hx,door_y-1,865),(8.75,1,8.75))
for i,x in enumerate([15,W-19.6]):
    # Side bead faces in YZ plane, 12mm thickness in X.
    for y in [PY,D-PY-B]:box(f'SIDE{i}_bead_V{y}',x-4,y,Z0,12,B,Z1-Z0,maple)
    for z in [Z0,Z1-B]:box(f'SIDE{i}_bead_H{z}',x-4,PY+B,z,12,D-2*PY-2*B,B,maple)
    reeded(f'SIDE{i}_GLASS',[x,PY+B,Z0+B],D-2*PY-2*B,Z1-Z0-2*B,True)

(OUT/'geometry_mm.json').write_text(json.dumps({'revision':'D16','source':'D15 with original DXF derived 30x40 upper posts and mating-panel adjustments','parameters':p,'parts':parts},separators=(',',':')),encoding='utf-8')
# Bounds exclude concept handles; ensure cabinet dimensions correspond to the CAD envelope.
verts=[v for part in parts if not part['name'].startswith('HANDLE') for v in part['vertices_mm']]
lo=[min(v[k] for v in verts) for k in range(3)];hi=[max(v[k] for v in verts) for k in range(3)]
assert all(abs((hi[k]-lo[k])-val)<1e-6 for k,val in enumerate([W,p['closed_depth'],H])),(lo,hi)

# Export the actual model without stage/cameras for independent orbit inspection.
bpy.ops.object.select_all(action='DESELECT')
for obj in collection.objects:obj.select_set(True)
bpy.context.view_layer.objects.active=next(iter(collection.objects))
bpy.ops.export_scene.gltf(filepath=str(OUT/'CB001_D16.glb'),use_selection=True,export_apply=True)

# Photographic stage; all cameras render exactly the same saved mesh.
ground=bpy.data.materials.new('Studio floor');ground.diffuse_color=(.8,.79,.75,1)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));floor=bpy.context.object;floor.name='STUDIO_FLOOR';floor.data.materials.append(ground)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.cycles.max_bounces=12;scene.cycles.transmission_bounces=8
scene.world.color=(.3,.3,.3)
scene.view_settings.view_transform='AgX'
def area(name,pos,power,size):
    bpy.ops.object.light_add(type='AREA',location=pos);ob=bpy.context.object;ob.name=name;ob.data.energy=power;ob.data.shape='DISK';ob.data.size=size
    ob.rotation_euler=(Vector((.34,.2,.75))-ob.location).to_track_quat('-Z','Y').to_euler()
area('Key',(-2,-3,3.5),500,3);area('Fill',(2,-1,2.8),300,2);area('Rim',(1,2,3),400,2)
def camera(name,pos,target,scale):
    bpy.ops.object.camera_add(location=pos);cam=bpy.context.object;cam.name=name;cam.data.type='ORTHO';cam.data.ortho_scale=scale
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();return cam
cams=[('perspective',camera('CAM_3quarter',(-2.2,-3.4,2.05),(.34,.18,.74),1.85)),
      ('front',camera('CAM_FRONT',(.3425,-4,.715),(.3425,0,.715),1.7)),
      ('side',camera('CAM_SIDE',(-4,.185,.715),(0,.185,.715),1.7)),
      ('top',camera('CAM_TOP',(.3425,.16,4),(.3425,.16,0),.9)),
      ('handles',camera('CAM_HANDLES',(.75,-1.3,1.02),(.3425,-.04,.865),.19)),
      ('detail',camera('CAM_DETAIL',(-1,-2,.85),(.065,.055,.285),.47))]
scene.render.resolution_x=1200;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
scene.camera=cams[0][1]
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CB001_D16.blend'))
print('D16 MODEL COMPLETE',OUT)
