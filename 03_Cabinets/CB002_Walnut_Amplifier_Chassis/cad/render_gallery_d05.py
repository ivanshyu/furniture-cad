# -*- coding: utf-8 -*-
"""Export CB002_D05.glb and render the 7 cabinet-style gallery views for the interactive viewer."""
import bpy, math, shutil
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'D05'
GAL = OUT / 'gallery'
GAL.mkdir(exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=str(OUT / 'CB002_D05.blend'))

# Export GLB of the full assembled model (excluding Studio_Floor)
floor = bpy.data.objects.get('Studio_Floor')
if floor:
    floor.select_set(False)
for o in bpy.data.objects:
    o.select_set(o.type == 'MESH' and o.name != 'Studio_Floor')
bpy.ops.export_scene.gltf(
    filepath=str(OUT / 'CB002_D05.glb'),
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)
print('GLB EXPORTED:', OUT / 'CB002_D05.glb', flush=True)

# Copy existing high-res renders into gallery views where applicable, and render remaining preset views
shutil.copy2(OUT / '01_assembled.png', GAL / 'persp_ai.png')
shutil.copy2(OUT / '01_assembled.png', GAL / 'persp_cad.png')
shutil.copy2(OUT / '04_underside_fixings.png', GAL / 'bottom_ai.png')
shutil.copy2(OUT / '04_underside_fixings.png', GAL / 'bottom_cad.png')
shutil.copy2(OUT / '05_stepped_wood_frame.png', GAL / 'frame_ai.png')
shutil.copy2(OUT / '05_stepped_wood_frame.png', GAL / 'frame_cad.png')
shutil.copy2(OUT / '02_exploded.png', GAL / 'exploded_ai.png')
shutil.copy2(OUT / '03_dimensions_and_fixings.png', GAL / 'sheet_ai.png')

scene = bpy.context.scene
scene.cycles.samples = 32
scene.render.resolution_x = 1200
scene.render.resolution_y = 900

cam = scene.camera
cam.data.type = 'PERSP'
cam.data.lens = 58.0


def aim(obj, pt):
    obj.rotation_euler = (Vector(pt) - obj.location).to_track_quat('-Z', 'Y').to_euler()


extra_views = {
    'front': ((0.26, -0.98, 0.14), (0.26, 0.19, 0.045), 58.0),
    'side': ((-0.78, 0.19, 0.16), (0.26, 0.19, 0.045), 58.0),
    'top': ((0.26, -0.08, 1.05), (0.26, 0.19, 0.045), 55.0),
    'detail': ((0.66, -0.28, 0.15), (0.48, 0.04, 0.045), 85.0),
}

if floor:
    floor.hide_render = False
    floor.location = (0.26, 0.19, -0.0141)

for name, (pos, target, lens) in extra_views.items():
    cam.data.lens = lens
    cam.location = pos
    aim(cam, target)
    out_file = GAL / f'{name}_ai.png'
    scene.render.filepath = str(out_file)
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_file, GAL / f'{name}_cad.png')
    print('GALLERY VIEW DONE:', name, flush=True)
