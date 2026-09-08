# -*- coding: utf-8 -*-
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]/'03_Cabinets/CB001_Curiosity_Low_Maple_Walnut/models/D16'
O=R/'gallery';O.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'CB001_D16.blend'))
s=bpy.context.scene;s.cycles.samples=16;s.cycles.adaptive_threshold=.06
s.render.resolution_x=800;s.render.resolution_y=880
c=s.camera;c.data.type='PERSP';c.data.sensor_fit='VERTICAL';c.data.sensor_height=32;c.data.lens=32/(2*math.tan(math.radians(35)/2))
views={'persp':([-2,-3,1.9],[.3425,.17,.715]),'front':([.3425,-3.4,.715],[.3425,.17,.715]),'side':([-3,.20233,.715],[.3425,.17,.715]),'top':([.3425,.20233,3.4],[.3425,.17,.715]),'detail':([-.35,-.75,.55],[.08,.055,.22]),'handles':([.65,-.8,.97],[.3425,-.04,.865]),'bottom':([1,-1,-.6],[.3425,.185,.305])}
for name,(pos,target) in views.items():
 c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler()
 bpy.data.objects['STUDIO_FLOOR'].hide_render=name=='bottom'
 s.render.filepath=str(O/f'{name}_cad.png');bpy.ops.render.render(write_still=True)
 print('VIEW COMPLETE',name,flush=True)
print('GALLERY DONE',flush=True)
