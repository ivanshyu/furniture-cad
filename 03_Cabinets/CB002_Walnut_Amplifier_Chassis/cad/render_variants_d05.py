# -*- coding: utf-8 -*-
"""Render missing material combinations in Blender Cycles using the exact D05 scene."""
import bpy
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'D05'
GAL = OUT / 'gallery'
GAL.mkdir(exist_ok=True)

blend_file = OUT / 'CB002_D05.blend'
bpy.ops.wm.open_mainfile(filepath=str(blend_file))

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.resolution_x = 1600
scene.render.resolution_y = 1150
scene.render.resolution_percentage = 100

# Camera
cam = scene.camera
cam.data.type = 'PERSP'
cam.data.lens = 58.0
cam.location = (0.86, -0.76, 0.40)


def aim(obj, pt):
    obj.rotation_euler = (Vector(pt) - obj.location).to_track_quat('-Z', 'Y').to_euler()


aim(cam, (0.26, 0.18, 0.040))


# Helper to build procedural wood shader
def make_wood_mat(name, base_rgb, dark_rgb, roughness=0.34, grain_scale=42.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Roughness'].default_value = roughness
    if 'Coat Weight' in bs.inputs:
        bs.inputs['Coat Weight'].default_value = 0.15
        bs.inputs['Coat Roughness'].default_value = 0.22

    coord = n.new('ShaderNodeTexCoord')
    mapping = n.new('ShaderNodeVectorMath')
    mapping.operation = 'MULTIPLY'
    mapping.inputs[1].default_value = (1.4, grain_scale, 36.0)
    l.new(coord.outputs['Object'], mapping.inputs[0])

    wave = n.new('ShaderNodeTexWave')
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'Z'
    wave.inputs['Scale'].default_value = 1.1
    wave.inputs['Distortion'].default_value = 5.5
    wave.inputs['Detail'].default_value = 4.0
    l.new(mapping.outputs['Vector'], wave.inputs['Vector'])

    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 8.0
    l.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.18
    ramp.color_ramp.elements[0].color = (*dark_rgb, 1.0)
    ramp.color_ramp.elements[1].position = 0.72
    ramp.color_ramp.elements[1].color = (*base_rgb, 1.0)
    l.new(wave.outputs['Color'], ramp.inputs['Fac'])
    l.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    return m


# Helper to build procedural metal shader
def make_metal_mat(name, base_rgb, roughness=0.25, metallic=0.92):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*base_rgb, 1.0)
    bs.inputs['Roughness'].default_value = roughness
    bs.inputs['Metallic'].default_value = metallic

    coord = n.new('ShaderNodeTexCoord')
    mapping = n.new('ShaderNodeVectorMath')
    mapping.operation = 'MULTIPLY'
    mapping.inputs[1].default_value = (400.0, 1.5, 400.0)
    l.new(coord.outputs['Object'], mapping.inputs[0])

    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 120.0
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.7
    l.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.012
    bump.inputs['Distance'].default_value = 0.001
    l.new(noise.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], bs.inputs['Normal'])
    return m


# Materials
mat_teak = make_wood_mat('Variant_Teak', (0.42, 0.23, 0.08), (0.18, 0.08, 0.02), roughness=0.32, grain_scale=42.0)
mat_walnut = make_wood_mat('Variant_Walnut', (0.16, 0.07, 0.03), (0.05, 0.02, 0.01), roughness=0.34, grain_scale=48.0)
mat_maple = make_wood_mat('Variant_Maple', (0.78, 0.69, 0.54), (0.64, 0.53, 0.38), roughness=0.36, grain_scale=55.0)

mat_brass = make_metal_mat('Variant_Brass', (0.76, 0.58, 0.26), roughness=0.22, metallic=0.92)
mat_silver = make_metal_mat('Variant_Silver', (0.68, 0.70, 0.72), roughness=0.22, metallic=0.94)
mat_black = make_metal_mat('Variant_Black', (0.018, 0.018, 0.020), roughness=0.32, metallic=0.88)

# Splines contrasting materials
mat_spline_walnut = make_wood_mat('Variant_Spline_Walnut', (0.14, 0.06, 0.02), (0.04, 0.015, 0.005), roughness=0.35)
mat_spline_maple = make_wood_mat('Variant_Spline_Maple', (0.80, 0.72, 0.58), (0.68, 0.58, 0.42), roughness=0.35)

configs = [
    ('persp_ai_teak_black.png', mat_teak, mat_spline_walnut, mat_black),
    ('persp_ai_walnut_black.png', mat_walnut, mat_spline_maple, mat_black),
    ('persp_ai_maple_black.png', mat_maple, mat_spline_walnut, mat_black),
    ('persp_ai_maple_brass.png', mat_maple, mat_spline_walnut, mat_brass),
]

all_objs = [o for o in scene.objects if o.type == 'MESH']
# Reset all to assembled
for o in all_objs:
    o.hide_render = False
    if 'ExplodedOffset_mm' in o:
        o.location = (0.0, 0.0, 0.0)

floor = bpy.data.objects.get('Studio_Floor')
if floor:
    floor.hide_render = False
    floor.location = (0.26, 0.19, -0.0141)

for out_name, wood_m, spline_m, metal_m in configs:
    for o in all_objs:
        if o.name.startswith(('W0', 'CB0')):
            o.data.materials.clear()
            o.data.materials.append(wood_m)
        elif o.name.startswith('SP0'):
            o.data.materials.clear()
            o.data.materials.append(spline_m)
        elif o.name.startswith(('A0', 'F0')):
            o.data.materials.clear()
            o.data.materials.append(metal_m)

    out_file = GAL / out_name
    scene.render.filepath = str(out_file)
    bpy.ops.render.render(write_still=True)
    print('RENDERED VARIANT:', out_name, flush=True)

print('ALL 4 MISSING VARIANTS RENDERED SUCCESSFULLY!', flush=True)
