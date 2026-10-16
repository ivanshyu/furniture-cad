import bpy, json, math, bmesh, os
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'D05'

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = False
scene.render.resolution_x = 1600
scene.render.resolution_y = 1150
scene.render.resolution_percentage = 100
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get('Background')
if bg:
    bg.inputs[0].default_value = (0.04, 0.042, 0.048, 1.0)
    bg.inputs[1].default_value = 0.65
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'


def make_teak_material(name, grain_axis='X'):
    """Procedural Burmese Teak (Tectona grandis): warm golden-amber brown with dark golden-brown straight oil streaks."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Roughness'].default_value = 0.28
    if 'Specular IOR Level' in bs.inputs:
        bs.inputs['Specular IOR Level'].default_value = 0.42
    if 'Coat Weight' in bs.inputs:
        bs.inputs['Coat Weight'].default_value = 0.18
        bs.inputs['Coat Roughness'].default_value = 0.20

    coord = n.new('ShaderNodeTexCoord')
    mapping = n.new('ShaderNodeVectorMath')
    mapping.operation = 'MULTIPLY'
    if grain_axis == 'X':
        mapping.inputs[1].default_value = (1.4, 42.0, 36.0)
    else:
        mapping.inputs[1].default_value = (42.0, 1.4, 36.0)
    l.new(coord.outputs['Object'], mapping.inputs[0])

    wave = n.new('ShaderNodeTexWave')
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'Z'
    wave.wave_profile = 'SIN'
    wave.inputs['Scale'].default_value = 1.05
    wave.inputs['Distortion'].default_value = 6.2
    wave.inputs['Detail'].default_value = 5.0
    wave.inputs['Detail Scale'].default_value = 1.8
    l.new(mapping.outputs['Vector'], wave.inputs['Vector'])

    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 22.0
    noise.inputs['Detail'].default_value = 6.0
    noise.inputs['Roughness'].default_value = 0.68
    l.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    mix_fac = n.new('ShaderNodeMath')
    mix_fac.operation = 'MULTIPLY_ADD'
    mix_fac.inputs[1].default_value = 0.42
    l.new(wave.outputs['Fac'], mix_fac.inputs[0])
    l.new(noise.outputs['Fac'], mix_fac.inputs[2])

    ramp = n.new('ShaderNodeValToRGB')
    # Burmese Teak: rich golden honey brown with characteristic dark mineral/oil streaks
    ramp.color_ramp.elements[0].position = 0.16
    ramp.color_ramp.elements[0].color = (0.075, 0.028, 0.006, 1.0)
    e_mid = ramp.color_ramp.elements.new(0.52)
    e_mid.color = (0.215, 0.088, 0.022, 1.0)
    ramp.color_ramp.elements[2].position = 0.88
    ramp.color_ramp.elements[2].color = (0.340, 0.155, 0.042, 1.0)

    l.new(mix_fac.outputs['Value'], ramp.inputs[0])
    l.new(ramp.outputs['Color'], bs.inputs['Base Color'])

    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.045
    bump.inputs['Distance'].default_value = 0.001
    l.new(noise.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], bs.inputs['Normal'])
    return m


def make_walnut_spline_material(name):
    """Procedural American Black Walnut (Juglans nigra) for corner splines: deep chocolate brown."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Roughness'].default_value = 0.30
    if 'Coat Weight' in bs.inputs:
        bs.inputs['Coat Weight'].default_value = 0.15
        bs.inputs['Coat Roughness'].default_value = 0.22

    coord = n.new('ShaderNodeTexCoord')
    mapping = n.new('ShaderNodeVectorMath')
    mapping.operation = 'MULTIPLY'
    mapping.inputs[1].default_value = (18.0, 18.0, 55.0)
    l.new(coord.outputs['Object'], mapping.inputs[0])

    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 14.0
    noise.inputs['Detail'].default_value = 5.0
    l.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.2
    ramp.color_ramp.elements[0].color = (0.014, 0.005, 0.002, 1.0)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.045, 0.018, 0.007, 1.0)
    l.new(noise.outputs['Fac'], ramp.inputs[0])
    l.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    return m


def make_brushed_brass():
    m = bpy.data.materials.new('Brushed_Brass_Gold')
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (0.82, 0.63, 0.28, 1.0)
    bs.inputs['Metallic'].default_value = 0.96
    coord = n.new('ShaderNodeTexCoord')
    scale = n.new('ShaderNodeVectorMath')
    scale.operation = 'MULTIPLY'
    scale.inputs[1].default_value = (1.5, 220.0, 220.0)
    l.new(coord.outputs['Object'], scale.inputs[0])

    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 35.0
    noise.inputs['Detail'].default_value = 5.0
    l.new(scale.outputs['Vector'], noise.inputs['Vector'])

    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.20, 0.20, 0.20, 1.0)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.28, 0.28, 0.28, 1.0)
    l.new(noise.outputs['Fac'], ramp.inputs[0])
    l.new(ramp.outputs['Color'], bs.inputs['Roughness'])

    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.015
    bump.inputs['Distance'].default_value = 0.0005
    l.new(noise.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], bs.inputs['Normal'])
    return m


def make_metal(name, color, roughness=0.25, metal=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1.0)
    bs.inputs['Metallic'].default_value = metal
    bs.inputs['Roughness'].default_value = roughness
    return m


teak_x = make_teak_material('Burmese_Teak_X', 'X')
teak_y = make_teak_material('Burmese_Teak_Y', 'Y')
walnut_spline = make_walnut_spline_material('Black_Walnut_Spline')
brass = make_brushed_brass()
brass_nut = make_metal('Brass_Nut', (0.85, 0.58, 0.18), 0.25, 0.92)
steel = make_metal('Stainless_Steel', (0.62, 0.66, 0.72), 0.24, 0.90)

objects = []
for p in json.loads((OUT / 'mesh_scene.json').read_text()):
    mesh = bpy.data.meshes.new(p['name'])
    mesh.from_pydata([[a / 1000.0 for a in v] for v in p['vertices']], [], p['faces'])
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(p['name'], mesh)
    scene.collection.objects.link(obj)
    nm = p['name']
    if nm.startswith(('W01', 'W02')):
        obj.data.materials.append(teak_x)
    elif nm.startswith(('W03', 'W04', 'CB0')):
        obj.data.materials.append(teak_y)
    elif nm.startswith('SP0'):
        obj.data.materials.append(walnut_spline)
    elif nm.startswith(('A0', 'F0')):
        obj.data.materials.append(brass)
    elif 'SquareNut' in nm:
        obj.data.materials.append(brass_nut)
    else:
        obj.data.materials.append(steel)

    mod = obj.modifiers.new('EdgeBevel', 'BEVEL')
    mod.width = 0.00035
    mod.segments = 2
    mod.limit_method = 'ANGLE'
    mod.angle_limit = 0.45
    obj['ExplodedOffset_mm'] = p['offset']
    objects.append(obj)

floor_mat = make_metal('Dark_Glossy_Tabletop', (0.02, 0.02, 0.022), roughness=0.16, metal=0.1)
bpy.ops.mesh.primitive_plane_add(size=20.0, location=(0.26, 0.19, -0.0141))
floor_obj = bpy.context.object
floor_obj.name = 'Studio_Floor'
floor_obj.data.materials.append(floor_mat)


def aim(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat('-Z', 'Y').to_euler()


lights_cfg = [
    ('Key_Warm', (0.15, -0.65, 0.95), 55.0, 1.1, (1.0, 0.95, 0.88)),
    ('Fill_Soft', (-0.75, -0.25, 0.55), 32.0, 1.3, (0.92, 0.95, 1.0)),
    ('Rim_Back', (0.85, 0.85, 0.80), 65.0, 0.9, (1.0, 0.92, 0.82)),
    ('Front_Grazing', (0.45, -0.95, 0.18), 28.0, 0.7, (1.0, 0.96, 0.90)),
]
light_objs = []
for name, loc, power, size, col in lights_cfg:
    data = bpy.data.lights.new(name, 'AREA')
    data.energy = power
    data.shape = 'DISK'
    data.size = size
    data.color = col
    o = bpy.data.objects.new(name, data)
    scene.collection.objects.link(o)
    o.location = loc
    aim(o, (0.26, 0.19, 0.045))
    light_objs.append(o)

cam_data = bpy.data.cameras.new('Camera')
cam = bpy.data.objects.new('Camera', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam_data.type = 'PERSP'
cam_data.lens = 58.0

# 1. Assembled Hero View
cam.location = (0.86, -0.76, 0.40)
aim(cam, (0.26, 0.18, 0.040))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'CB002_D05.blend'))
scene.render.filepath = str(OUT / '01_assembled.png')
bpy.ops.render.render(write_still=True)

# 2. Exploded Assembly View
for o in objects:
    o.location = Vector(o['ExplodedOffset_mm']) / 1000.0
floor_obj.location = (0.26, 0.19, -0.065)
cam.location = (1.15, -1.12, 0.78)
aim(cam, (0.26, 0.19, 0.045))
scene.render.filepath = str(OUT / '02_exploded.png')
bpy.ops.render.render(write_still=True)

# Reset positions to assembled
for o in objects:
    o.location = (0.0, 0.0, 0.0)

# 3. Underside Fixings & 10-Point All-Wall Embedded Square Nut View
floor_obj.hide_render = True
for lo in light_objs:
    lo.hide_render = True
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 0.64
cam.location = (0.26, 0.14, -0.85)
aim(cam, (0.26, 0.19, 0.045))
u_light1 = bpy.data.lights.new('Underside_Key', 'AREA')
u_light1.energy = 14.0
u_light1.size = 1.2
u_ob1 = bpy.data.objects.new('Underside_Key', u_light1)
scene.collection.objects.link(u_ob1)
u_ob1.location = (0.10, -0.25, -0.65)
aim(u_ob1, (0.26, 0.19, 0.05))

u_light2 = bpy.data.lights.new('Underside_Fill', 'AREA')
u_light2.energy = 10.0
u_light2.size = 1.2
u_ob2 = bpy.data.objects.new('Underside_Fill', u_light2)
scene.collection.objects.link(u_ob2)
u_ob2.location = (0.45, 0.55, -0.65)
aim(u_ob2, (0.26, 0.19, 0.05))

scene.render.filepath = str(OUT / '04_underside_fixings.png')
bpy.ops.render.render(write_still=True)

# 4. Bare Stepped Burmese Teak Frame + Black Walnut Splines + Corner Blocks + 10 Embedded Square Nuts View
for o in objects:
    o.hide_render = not (o.name.startswith(('W0', 'SP0', 'CB0')) or 'SquareNut' in o.name)
floor_obj.hide_render = False
floor_obj.location = (0.26, 0.19, -0.0005)
u_ob1.hide_render = True
u_ob2.hide_render = True
for lo in light_objs:
    lo.hide_render = False
cam_data.type = 'PERSP'
cam_data.lens = 55.0
cam.location = (0.84, -0.74, 0.48)
aim(cam, (0.26, 0.19, 0.045))
scene.render.filepath = str(OUT / '05_stepped_wood_frame.png')
bpy.ops.render.render(write_still=True)
