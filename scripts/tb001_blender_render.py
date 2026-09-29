"""Import exact FreeCAD tessellation and render procedural wood; no AI or remodelling.
Run Blender --background --python scripts/tb001_blender_render.py.
"""
import bpy, json, math, hashlib, re, os
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('TB001_D07_OUT',str(ROOT/'02_Tables/TB001_D16_Three_Tier/models/D07/variants/snug_slot_20')))
G=OUT/'gallery';G.mkdir(exist_ok=True)
data=json.loads((OUT/'geometry_mm.json').read_text());views=json.loads((OUT/'views.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.06
s.render.resolution_x=900;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.film_transparent=False
s.view_settings.view_transform='AgX';s.view_settings.exposure=0;s.view_settings.look='AgX - Medium High Contrast'
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.78,.79,.8,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.35

# Keep the studio background neutral in orthographic/underside cameras without
# increasing environment illumination on the wood.
wn=s.world.node_tree.nodes;wl=s.world.node_tree.links;lp=wn.new('ShaderNodeLightPath');bg=wn.new('ShaderNodeBackground');bg.inputs[0].default_value=(1.0,.98,.94,1);bg.inputs[1].default_value=1.0
mix=wn.new('ShaderNodeMixShader');wl.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);wl.new(wn['Background'].outputs[0],mix.inputs[1]);wl.new(bg.outputs[0],mix.inputs[2]);wl.new(mix.outputs[0],wn['World Output'].inputs['Surface'])

def linear(hexcode):
 rgb=[int(hexcode[i:i+2],16)/255 for i in (0,2,4)]
 return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1,)
def wood(name,a,b):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.48
 attr=n.new('ShaderNodeAttribute');attr.attribute_name='wood_coord'
 scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(8,480,200);l.new(attr.outputs['Vector'],scale.inputs[0])
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2;noise.inputs['Roughness'].default_value=.65;l.new(scale.outputs['Vector'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=linear(a);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=linear(b);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],bs.inputs['Base Color'])
 return m
mats={'MAPLE':wood('MAPLE — pale closed-grain / illustrative','cbb99b','e3d5bc'),'WALNUT':wood('WALNUT — subdued straight grain / illustrative','342218','5c3d28')}
objects=[]
def direction(p):
 role=p['group'];name=p['name']
 if 'grain_angle_deg' in p:
  a=math.radians(p['grain_angle_deg']);return Vector((math.cos(a),math.sin(a),0))
 if role in ('leg','slot_trim') and 'lintel' not in name:return Vector((0,0,1))
 if role in ('upper_top','lower_top'):return Vector((1,0,0))
 if role=='grip_trim':return Vector((0,1,0)) if any(v in name for v in ['east','west']) else Vector((1,0,0))
 if role=='x_rail':angle=45 if 'beam 1' in name else 135
 else:
  match=re.search(r'(?<!\d)(30|45|135|150|225|270|315)(?!\d)',name);angle=(int(match.group()) if match else 0)+90
 return Vector((math.cos(math.radians(angle)),math.sin(math.radians(angle)),0))
for p in data['parts']:
 mesh=bpy.data.meshes.new(p['id']);verts=[tuple(x/1000 for x in v) for v in p['vertices_mm']];mesh.from_pydata(verts,[],p['faces']);mesh.update()
 obj=bpy.data.objects.new(p['id']+' '+p['name'],mesh);bpy.context.collection.objects.link(obj);obj.data.materials.append(mats[p['material']]);obj['role']=p['group'];obj['source_part_id']=p['id'];objects.append(obj)
 along=direction(p);across=along.cross(Vector((0,0,1))) if abs(along.z)<.9 else Vector((1,0,0));across.normalize();normal=along.cross(across).normalized()
 attr=mesh.attributes.new(name='wood_coord',type='FLOAT_VECTOR',domain='POINT')
 for i,v in enumerate(verts):
  v=Vector(v);attr.data[i].vector=(v.dot(along),v.dot(across),v.dot(normal))
 # Preserve exact vertex positions. Only shading normals become smooth at shallow angles.
 for face in mesh.polygons:face.use_smooth=True
 mesh.set_sharp_from_angle(angle=math.radians(30))
 assert len(mesh.vertices)==len(verts)
 assert max((mesh.vertices[i].co-Vector(v)).length for i,v in enumerate(verts))<1e-7
# Studio objects never included in source geometry checks.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));floor=bpy.context.object;floor.name='STUDIO_FLOOR'
fmat=bpy.data.materials.new('Neutral studio');fmat.use_nodes=True;fmat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=linear('eeeae3');fmat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.8;floor.data.materials.append(fmat)
def area(name,loc,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.27))-o.location).to_track_quat('-Z','Y').to_euler();return o
area('KEY',(-2,-3,4),450,3);area('FILL',(3,-1,2),180,3);area('RIM',(0,3,3),220,2.5)
cdata=bpy.data.cameras.new('Fixed CAD cameras');cam=bpy.data.objects.new('CAMERA',cdata);bpy.context.collection.objects.link(cam);s.camera=cam

def setup(name,spec):
 cam.location=spec['position'];target=Vector(spec['target']);toward=(cam.location-target).normalized();right=Vector(spec['up']).cross(toward).normalized();up=toward.cross(right).normalized();cam.rotation_euler=Matrix((right,up,toward)).transposed().to_euler()
 aspect=s.render.resolution_x/s.render.resolution_y;span=spec['span']*max(1,1/aspect)
 cdata.sensor_fit='VERTICAL';cdata.sensor_height=32;cdata.clip_start=.001;cdata.clip_end=300
 if spec.get('projection')=='perspective':cdata.type='PERSP';cdata.lens=32*(cam.location-target).length/span
 else:cdata.type='ORTHO';cdata.ortho_scale=span
 for obj in objects:obj.hide_render=name=='structure' and obj['role'] in ('upper_top','lower_top','grip_trim')
 floor.hide_render=name=='bottom'
setup('perspective',views['perspective']);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'TB001_D07_materials.blend'))
hashfile=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
manifest={'renderer':'Blender '+bpy.app.version_string+' / Cycles / 24 samples / denoised','not_ai':True,'geometry_sha256':hashfile(OUT/'geometry_mm.json'),'views_sha256':hashfile(OUT/'views.json'),'script_sha256':hashfile(Path(__file__)),'part_count':len(objects),'vertex_positions_preserved':True,'materials':'Procedural illustrative maple/walnut; not scanned wood or verified finish','views':{}}
for name,spec in views.items():
 setup(name,spec);s.render.filepath=str(G/f'{name}_blender.png');bpy.ops.render.render(write_still=True)
 manifest['views'][name]={'camera':spec,'output':f'{name}_blender.png','sha256':hashfile(G/f'{name}_blender.png')};print('COMPLETE',name,flush=True)
setup('perspective',views['perspective']);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'TB001_D07_materials.blend'))
manifest['blend_sha256']=hashfile(OUT/'TB001_D07_materials.blend');(G/'blender_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('ALL SEVEN VIEWS COMPLETE',flush=True)
