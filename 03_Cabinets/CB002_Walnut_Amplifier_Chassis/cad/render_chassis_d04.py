import bpy,json,math,bmesh,os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output'/'D04'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.render.resolution_x=1500;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.world.color=(.18,.18,.18)
scene.view_settings.view_transform='AgX'
def mat(name,color,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=.3 if metal else .4
 return m
wood=mat('Walnut - procedural illustrative grain',(.19,.075,.028))
n=wood.node_tree.nodes;l=wood.node_tree.links;bs=n.get('Principled BSDF')
tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=3;tex.inputs['Detail'].default_value=3;tex.inputs['Roughness'].default_value=.7
coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(3,120,95)
l.new(coord.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs['Vector'],tex.inputs['Vector'])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.2;ramp.color_ramp.elements[0].color=(.045,.014,.006,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(.28,.115,.043,1)
l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],bs.inputs['Base Color'])
gold=mat('Gold anodised aluminium - appearance only',(.65,.43,.16),.8);steel=mat('Steel hardware',(.25,.28,.32),.75);dowel=mat('Wood dowel',(.42,.24,.1))
objects=[]
for p in json.loads((OUT/'mesh_scene.json').read_text()):
 mesh=bpy.data.meshes.new(p['name']);mesh.from_pydata([[a/1000 for a in v] for v in p['vertices']],[],p['faces']);mesh.update()
 bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.0000001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
 obj=bpy.data.objects.new(p['name'],mesh);scene.collection.objects.link(obj)
 obj.data.materials.append(wood if p['name'].startswith('W0') else gold if p['name'].startswith(('A0','I0')) else dowel if p['name'].startswith(('FD','RD')) else steel)
 mod=obj.modifiers.new('Tiny illustrative edge highlight','BEVEL');mod.width=.00025;mod.segments=2;mod.limit_method='ANGLE';mod.angle_limit=.4
 obj['ExplodedOffset_mm']=p['offset'];objects.append(obj)
floor=mat('Warm neutral studio',(.12,.14,.16))
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.004));bpy.context.object.data.materials.append(floor)
def aim(obj,point):obj.rotation_euler=(Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()
for name,loc,power,size in [('Key',(.2,-.4,1.1),100,1),('Fill',(-.6,.3,.5),70,.8),('Rim',(.7,.8,.8),130,.6)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=power*.55;data.shape='DISK';data.size=size;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=loc;aim(o,(.26,.19,.04))
data=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO';data.ortho_scale=.79;cam.location=(.91,-.84,.66);aim(cam,(.26,.19,.065));data.lens=50
# Text is placed as camera-facing overlay in real scene, outside product bounds.
def label(body,location,size):
 curve=bpy.data.curves.new('Caption','FONT');curve.body=body;curve.size=size;curve.extrude=0
 ob=bpy.data.objects.new('Caption',curve);scene.collection.objects.link(ob);ob.location=location;ob.rotation_euler=cam.rotation_euler;ob.data.materials.append(mat('Caption ink '+body[:6],(.72,.76,.8)));return ob
scene.render.filepath=str(OUT/'01_assembled.png');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CB002_D04.blend'));
if not os.environ.get('CB_UNDERSIDE_ONLY'):bpy.ops.render.render(write_still=True)
for o in objects:o.location=Vector(o['ExplodedOffset_mm'])/1000
cam.data.ortho_scale=.94;cam.location=(.99,-1.05,.9);aim(cam,(.26,.19,.095));scene.render.filepath=str(OUT/'02_exploded.png')
if not os.environ.get('CB_UNDERSIDE_ONLY'):bpy.ops.render.render(write_still=True)
# leave saved blend assembled; render depicts exploded derived from the same CAD mesh

for o in objects:o.location=(0,0,0)
# hide floor for underside inspection
for o in scene.objects:
 if o.name.startswith('Plane'):o.hide_render=True
cam.location=(.26,.19,-.9);aim(cam,(.26,.19,.05));cam.data.ortho_scale=.74
# underside fill
light=bpy.data.lights.new('Underside fill','AREA');light.energy=55;light.size=.8
ob=bpy.data.objects.new('Underside fill',light);scene.collection.objects.link(ob);ob.location=(.25,.05,-.5);aim(ob,(.26,.19,.06))
scene.render.filepath=str(OUT/'04_underside_fixings.png');bpy.ops.render.render(write_still=True)
