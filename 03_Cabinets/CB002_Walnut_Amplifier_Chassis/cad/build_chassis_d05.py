"""D05 concept — high-fidelity CAD reconstruction (Burmese Teak + Black Walnut 45-deg Mitered Splines + All-4-Wall Embedded Square Nut Bars + Protruding Panels).
Run with FreeCAD Python; master dimensions here, mm.
All dimensions are [ASSUMED] / [TO VERIFY] concept drafts, NOT factory production drawings.
"""
import FreeCAD as A, Part, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'D05'
OUT.mkdir(exist_ok=True)

# Master Envelope & Draft Parameters (mm) — [ASSUMED] / [DERIVED]
W, D, H, T = 520.0, 380.0, 90.0, 20.0
PW, PH, PT, R = 444.0, 64.0, 6.0, 8.0
REBATE_DEPTH = 4.0       # Outer panel pocket depth in wood (4.0mm recessed)
PANEL_PROTRUDE = 2.0     # Panel protrudes 2.0mm proud of wood face (PT = 4.0 + 2.0 = 6.0mm)
WOOD_SHOULDER_T = T - REBATE_DEPTH  # 16.0mm remaining solid wood thickness behind rebate!
WIN_W, WIN_H, WIN_R = 404.0, 48.0, 6.0  # Enlarged from 40mm to 48mm (Z=21..69) for ALPS RK50 & meters
SPLINE_Z = [21.0, 64.0]  # 2 Black Walnut splines per corner, 5.0mm thick (Z=21..26 and Z=64..69)
SPLINE_H = 5.0
SPLINE_LEG = 14.0        # Spline extends 14.0mm along both X and Y outer faces
TOP_LOWER_H = 8.0        # Lower tier of stepped top plate (Z=90..98)
TOP_UPPER_H = 5.0        # Upper tier of stepped top plate (Z=98..103, inset 10mm)
TOP_UPPER_INSET = 10.0
TOP_BOSS_H = 4.0         # Underside locating boss into wooden frame (Z=86..90)
FOOT_D, FOOT_H = 48.0, 14.0

V = A.Vector
doc = A.newDocument('CB002_D05')
parts = []
shapes = []

teak_col = (0.52, 0.31, 0.14)    # Burmese Teak (golden-amber brown)
walnut_col = (0.14, 0.06, 0.025) # American Black Walnut (deep chocolate brown for splines)
brass_col = (0.76, 0.58, 0.26)
steel_col = (0.62, 0.65, 0.68)


def box(w, d, h, x, y, z):
    return Part.makeBox(w, d, h, V(x, y, z))


def cyl(r, l, x, y, z, axis=(0, 0, 1)):
    return Part.makeCylinder(r, l, V(x, y, z), V(*axis))


def cone(r1, r2, l, x, y, z, axis=(0, 0, 1)):
    return Part.makeCone(r1, r2, l, V(x, y, z), V(*axis))


def poly_prism(pts_xy, z0, h):
    wire = Part.makePolygon([V(px, py, z0) for px, py in pts_xy] + [V(pts_xy[0][0], pts_xy[0][1], z0)])
    face = Part.Face(wire)
    return face.extrude(V(0, 0, h))


def rr_y(x, z, w, h, r, y, depth):
    """Rounded rectangle extruded along Y axis."""
    s = box(w - 2 * r, depth, h, x + r, y, z).fuse(box(w, depth, h - 2 * r, x, y, z + r))
    for xx in [x + r, x + w - r]:
        for zz in [z + r, z + h - r]:
            s = s.fuse(cyl(r, depth, xx, y, zz, (0, 1, 0)))
    return s.removeSplitter()


def rear(s):
    s = s.copy()
    s.rotate(V(W / 2, D / 2, 0), V(0, 0, 1), 180)
    return s


def add(name, s, color, offset=(0, 0, 0), material=''):
    s = s.removeSplitter()
    assert s.isValid() and s.Volume > 0, f"Invalid shape: {name}"
    o = doc.addObject('PartDesign::Feature', name)
    o.Label = name
    o.Shape = s
    o.addProperty('App::PropertyString', 'Evidence')
    o.Evidence = 'ASSUMED / TO VERIFY — D05 CONCEPT NOT FOR MANUFACTURE'
    o.addProperty('App::PropertyString', 'Material')
    o.Material = material
    o.addProperty('App::PropertyVector', 'ExplodedOffset')
    o.ExplodedOffset = V(*offset)
    if A.GuiUp:
        o.ViewObject.ShapeColor = color
    verts, tris = s.tessellate(0.12)
    parts.append(dict(
        name=name,
        color=color,
        offset=offset,
        vertices=[[round(v.x, 4), round(v.y, 4), round(v.z, 4)] for v in verts],
        faces=tris,
        volume=round(s.Volume, 2)
    ))
    shapes.append(o)
    return o


# ==============================================================================
# 1. FRONT & REAR 45-DEG MITERED BURMESE TEAK RAILS (W01, W02)
#    - 45° mitered corners: trapezoid X=0..W at Y=0, X=T..W-T at Y=T
#    - Corner spline slots at Z=21..26 and Z=64..69 (leg=14mm)
#    - Step 1: Outer panel rebate 444.6 x 64.6 x 4.0 (R8.3) -> 6mm plate protrudes 2.0mm!
#    - Step 2: Inner through-window 404.0 x 48.0 x 16.0 (R6.0) -> Z=21..69
#    - Perimeter wood shoulder retained (LR 20mm, TB 8mm, thickness 16mm)
#    - 6 through-holes (Ø3.4, no screw-head counterbores) at Z=45 (LR) and Z=17, 73 (TB)
#    - Top inner rabbet step (Z=86..90) + 2 drop-in square nut mortises at X=185, 335 (per S04!)
# ==============================================================================
panel_x = (W - PW) / 2.0
panel_z = (H - PH) / 2.0
holes = (
    [(W / 2 - 214, H / 2), (W / 2 + 214, H / 2)] +
    [(x, H / 2 + z) for x in [W / 2 - 140, W / 2 + 140] for z in [-28, 28]]
)
front_nut_xs = [185.0, W - 185.0]  # X=185, 335 on front/rear rails

# 45-deg mitered front rail base prism
front = poly_prism([(0.0, 0.0), (W, 0.0), (W - T, T), (T, T)], 0.0, H)

# Cut corner spline slots at front-left (0,0) and front-right (W,0)
fl_spline_cut = poly_prism([(-0.5, -0.5), (SPLINE_LEG + 0.5, -0.5), (-0.5, SPLINE_LEG + 0.5)], 0.0, SPLINE_H)
fr_spline_cut = poly_prism([(W + 0.5, -0.5), (W + 0.5, SPLINE_LEG + 0.5), (W - SPLINE_LEG - 0.5, -0.5)], 0.0, SPLINE_H)
for sz in SPLINE_Z:
    c1 = fl_spline_cut.copy(); c1.translate(V(0, 0, sz))
    c2 = fr_spline_cut.copy(); c2.translate(V(0, 0, sz))
    front = front.cut(c1).cut(c2)

# Step 1: Outer panel rebate (depth 4.0mm from Y=0 so 6mm panel protrudes 2.0mm proud)
front = front.cut(rr_y(panel_x - 0.3, panel_z - 0.3, PW + 0.6, PH + 0.6, R + 0.3, -0.1, REBATE_DEPTH + 0.1))
# Step 2: Inner wiring through-window (404x48, R6, through remaining 16mm wood Y=4..20)
front = front.cut(rr_y(W / 2 - WIN_W / 2, H / 2 - WIN_H / 2, WIN_W, WIN_H, WIN_R, REBATE_DEPTH - 0.1, WOOD_SHOULDER_T + 0.2))

# 6 M3 clearance holes through the 16mm wood shoulder (no counterbore)
for x, z in holes:
    front = front.cut(cyl(1.7, T + 2, x, -1, z, (0, 1, 0)))

# Top inner rabbet step along front/rear rail (Z=86..90.1, X=T..W-T, Y=9.5..20.1)
front = front.cut(box(W - 2 * T, 10.6, 4.1, T, 9.5, 86.0))

# 2 Drop-in vertical blind mortises in front/rear top rail (from Z=86 down to Z=70.5 at X=185, 335)
# Leaves 6.0mm inner wood shoulder (Y=14.0..20.0) and 5.5mm wood behind panel rebate (Y=4.0..9.5)
for xx in front_nut_xs:
    front = front.cut(box(22.0, 4.5, 15.6, xx - 11.0, 9.5, 70.5))
    for dx in [-6.0, 6.0]:
        front = front.cut(cyl(2.2, 12.0, xx + dx, 8.5, 75.5, (0, 1, 0)))

add('W01_Front_Teak', front, teak_col, (0, -55, 0),
    'Burmese Teak / grain X / 45-deg mitered spline joint + top-rabbet nut mortises')
add('W02_Rear_Teak', rear(front), teak_col, (0, 55, 0),
    'Burmese Teak / grain X / 45-deg mitered spline joint + top-rabbet nut mortises')

# ==============================================================================
# 2. LEFT & RIGHT 45-DEG MITERED BURMESE TEAK SIDE WALLS (W03, W04)
#    - 45° mitered corners complementary to W01/W02
#    - Corner spline slots at Z=21..26 and Z=64..69
#    - Top inner step at Z=86..90 for hidden vertical drop-in square nut bars
# ==============================================================================
side_nut_ys = [70.0, D / 2, D - 70.0]
top_pts = (
    [(37.0, y) for y in side_nut_ys] +
    [(W - 37.0, y) for y in side_nut_ys] +
    [(x, 37.0) for x in front_nut_xs] +
    [(x, D - 37.0) for x in front_nut_xs]
)

left_side = poly_prism([(0.0, 0.0), (T, T), (T, D - T), (0.0, D)], 0.0, H)
rl_spline_cut = poly_prism([(-0.5, D + 0.5), (-0.5, D - SPLINE_LEG - 0.5), (SPLINE_LEG + 0.5, D + 0.5)], 0.0, SPLINE_H)
for sz in SPLINE_Z:
    c1 = fl_spline_cut.copy(); c1.translate(V(0, 0, sz))
    c2 = rl_spline_cut.copy(); c2.translate(V(0, 0, sz))
    left_side = left_side.cut(c1).cut(c2)

# Top inner rabbet along side wall (Z=86..90.1, Y=T..D-T, X=9.5..20.1)
left_side = left_side.cut(box(10.6, D - 2 * T, 4.1, 9.5, T, 86.0))

# 3 Drop-in vertical blind mortises from Z=86 down to Z=68.5 for Dual-Hole Square Nut Bars
for yy in side_nut_ys:
    left_side = left_side.cut(box(4.5, 22.0, 17.6, 9.5, yy - 11.0, 68.5))
    for dy in [-6.0, 6.0]:
        left_side = left_side.cut(cyl(2.2, 12.0, 8.5, yy + dy, 72.0, (1, 0, 0)))

add('W03_Side_Teak', left_side, teak_col, (-55, 0, 0),
    'Burmese Teak / grain Y / 45-deg mitered spline joint & drop-in nut pockets')
add('W04_Side_Teak', rear(left_side), teak_col, (55, 0, 0),
    'Burmese Teak / grain Y / 45-deg mitered spline joint & drop-in nut pockets')

# ==============================================================================
# 3. FRONT & REAR PROTRUDING CHAMFERED BRASS/ALUMINIUM PLATES (A01, A02)
#    - 6.0mm thick: 4.0mm seated in wood rebate (Y=0..4.0), 2.0mm proud (Y=-2.0..0.0)
#    - 1.0mm front perimeter chamfer at Y=-2.0..-1.0
# ==============================================================================
plate_base = rr_y(panel_x, panel_z, PW, PH, R, -PANEL_PROTRUDE + 1.0, PT - 1.0)
plate_front = rr_y(panel_x + 0.8, panel_z + 0.8, PW - 1.6, PH - 1.6, R - 0.8, -PANEL_PROTRUDE, 1.0)
plate = plate_base.fuse(plate_front).removeSplitter()
for x, z in holes:
    plate = plate.cut(cyl(1.25, 4.0, x, REBATE_DEPTH, z, (0, -1, 0)))

add('A01_Front_Blank', plate, brass_col, (0, -115, 0),
    'Brushed Brass / Gold Anodised Aluminium 6mm (4mm recessed, 2mm proud of wood)')
add('A02_Rear_Blank', rear(plate), brass_col, (0, 115, 0),
    'Brushed Brass / Gold Anodised Aluminium 6mm (4mm recessed, 2mm proud of wood)')

# ==============================================================================
# 4. TWO-TIER STEPPED TOP PLATE WITH HIDDEN UNDERSIDE BOSS (A03)
#    - 10 underside M4 blind tapped holes (Left 3 + Right 3 + Front 2 + Rear 2)
# ==============================================================================
top_skirt = box(W, D, TOP_LOWER_H, 0, 0, H)
top_tier2 = box(W - 2 * TOP_UPPER_INSET, D - 2 * TOP_UPPER_INSET, TOP_UPPER_H - 0.8,
                TOP_UPPER_INSET, TOP_UPPER_INSET, H + TOP_LOWER_H)
top_tier2_cap = box(W - 2 * (TOP_UPPER_INSET + 0.8), D - 2 * (TOP_UPPER_INSET + 0.8), 0.8,
                    TOP_UPPER_INSET + 0.8, TOP_UPPER_INSET + 0.8, H + TOP_LOWER_H + TOP_UPPER_H - 0.8)
top_boss = box(W - 41.0, D - 41.0, TOP_BOSS_H, 20.5, 20.5, H - TOP_BOSS_H)
top = top_skirt.fuse(top_tier2).fuse(top_tier2_cap).fuse(top_boss).removeSplitter()

for x, y in top_pts:
    top = top.cut(cyl(1.65, 6.0, x, y, H - TOP_BOSS_H))

add('A03_Stepped_Hidden_Top', top, brass_col, (0, 0, 125),
    'Stepped Brushed Brass / Aluminium Top Plate (Lower 8 + Upper 5 + Boss 4, 10-Point Hidden Fixings)')

# ==============================================================================
# 5. FOUR CNC MACHINED FEET (F01..F04) — per S01/S03
# ==============================================================================
foot_coords = [(64.0, 38.0), (W - 64.0, 38.0), (64.0, D - 38.0), (W - 64.0, D - 38.0)]
for idx, (fx, fy) in enumerate(foot_coords):
    f_body = cyl(FOOT_D / 2, 12.0, fx, fy, -12.0).fuse(cone(FOOT_D / 2 - 2.0, FOOT_D / 2, 2.0, fx, fy, -14.0))
    groove = cyl(FOOT_D / 2 + 0.1, 1.0, fx, fy, -4.0).cut(cyl(FOOT_D / 2 - 0.8, 1.0, fx, fy, -4.0))
    f_body = f_body.cut(groove).cut(cyl(2.2, 14.2, fx, fy, -14.1))
    add(f'F0{idx+1}_Foot', f_body, brass_col, (0, 0, -45), 'CNC Machined Aluminium/Brass Foot Ø48x14 [ASSUMED]')

# ==============================================================================
# 6. FOUR INTERNAL BURMESE TEAK CORNER REINFORCEMENT BLOCKS (CB01..CB04)
#    - Chamfered 22x22x78mm solid Burmese Teak corner post inside each corner (Z=0..78)
#    - Reinforces the 45° mitered joint against racking/lifting loads (>41kg)
# ==============================================================================
cb_pts_fl = [(20.0, 20.0), (42.0, 20.0), (42.0, 28.0), (28.0, 42.0), (20.0, 42.0)]
cb_fl = poly_prism(cb_pts_fl, 0.0, 78.0)
cb_fr = poly_prism([(W - px, py) for px, py in reversed(cb_pts_fl)], 0.0, 78.0)
add('CB01_CornerBlock_FL', cb_fl, teak_col, (-25, -25, 0), 'Burmese Teak Internal Corner Reinforcement Block 22x22x78')
add('CB02_CornerBlock_FR', cb_fr, teak_col, (25, -25, 0), 'Burmese Teak Internal Corner Reinforcement Block 22x22x78')
add('CB03_CornerBlock_RR', rear(cb_fl), teak_col, (25, 25, 0), 'Burmese Teak Internal Corner Reinforcement Block 22x22x78')
add('CB04_CornerBlock_RL', rear(cb_fr), teak_col, (-25, 25, 0), 'Burmese Teak Internal Corner Reinforcement Block 22x22x78')

# ==============================================================================
# 7. EIGHT AMERICAN BLACK WALNUT CORNER SPLINES (SP01..SP08) — 2 per corner
# ==============================================================================
sp_fl_base = poly_prism([(0.0, 0.0), (SPLINE_LEG, 0.0), (0.0, SPLINE_LEG)], 0.0, SPLINE_H)
sp_fr_base = poly_prism([(W, 0.0), (W, SPLINE_LEG), (W - SPLINE_LEG, 0.0)], 0.0, SPLINE_H)
sp_idx = 1
for sz in SPLINE_Z:
    s1 = sp_fl_base.copy(); s1.translate(V(0, 0, sz))
    s2 = sp_fr_base.copy(); s2.translate(V(0, 0, sz))
    add(f'SP0{sp_idx}_Spline_FL', s1, walnut_col, (-38, -38, 0), 'American Black Walnut Corner Spline 14x14x5')
    add(f'SP0{sp_idx+1}_Spline_FR', s2, walnut_col, (38, -38, 0), 'American Black Walnut Corner Spline 14x14x5')
    add(f'SP0{sp_idx+2}_Spline_RR', rear(s1), walnut_col, (38, 38, 0), 'American Black Walnut Corner Spline 14x14x5')
    add(f'SP0{sp_idx+3}_Spline_RL', rear(s2), walnut_col, (-38, 38, 0), 'American Black Walnut Corner Spline 14x14x5')
    sp_idx += 4

# ==============================================================================
# 8A. LEFT & RIGHT SIDE L-BRACKETS, DROP-IN SQUARE NUT BARS & FASTENERS (LB0..2, RB0..2)
# ==============================================================================
for back in [False, True]:
    for j, y in enumerate(side_nut_ys):
        prefix = ('RB' if back else 'LB') + str(j)
        conv = rear if back else (lambda s: s)
        offset = (45 if back else -45, 0, 25)

        bracket = box(3.0, 24.0, 22.0, 20.0, y - 12.0, 64.0).fuse(
            box(28.0, 24.0, 3.0, 20.0, y - 12.0, 83.0)
        ).removeSplitter()
        slot_cut = (
            cyl(2.25, 5.0, 35.5, y, 82.0)
            .fuse(cyl(2.25, 5.0, 38.5, y, 82.0))
            .fuse(box(3.0, 4.5, 5.0, 35.5, y - 2.25, 82.0))
        )
        bracket = bracket.cut(slot_cut)
        for dy in [-6.0, 6.0]:
            bracket = bracket.cut(cyl(2.25, 5.0, 19.0, y + dy, 72.0, (1, 0, 0)))
        add(prefix + '_Bracket', conv(bracket), steel_col, offset, '3mm Stainless/Aluminium Side L-Bracket')

        washer_up = cyl(4.5, 1.0, 37.0, y, 82.0).cut(cyl(2.2, 1.0, 37.0, y, 82.0))
        screw_up = cyl(2.0, 8.0, 37.0, y, 82.0).fuse(cyl(3.5, 3.5, 37.0, y, 78.5))
        screw_up = screw_up.cut(cyl(1.5, 2.0, 37.0, y, 78.4))
        add(prefix + '_TopWasher', conv(washer_up), steel_col, (0, 0, -25))
        add(prefix + '_Up_M4x8', conv(screw_up), steel_col, (0, 0, -40))

        nut_bar = box(4.0, 20.0, 16.0, 9.7, y - 10.0, 69.0)
        for dy in [-6.0, 6.0]:
            nut_bar = nut_bar.cut(cyl(1.65, 4.2, 9.6, y + dy, 72.0, (1, 0, 0)))
        add(prefix + '_SquareNutBar', conv(nut_bar), brass_col, (0, 0, 35),
            'Drop-In Square Nut Bar 20x16x4 (M4x2) in side top-step blind mortise')

        for k, dy in enumerate([-6.0, 6.0]):
            washer_s = cyl(4.5, 1.0, 23.0, y + dy, 72.0, (1, 0, 0)).cut(
                cyl(2.2, 1.0, 23.0, y + dy, 72.0, (1, 0, 0))
            )
            screw_s = cyl(2.0, 14.0, 10.0, y + dy, 72.0, (1, 0, 0)).fuse(
                cyl(3.5, 3.0, 24.0, y + dy, 72.0, (1, 0, 0))
            )
            screw_s = screw_s.cut(cyl(1.5, 1.8, 25.3, y + dy, 72.0, (1, 0, 0)))
            add(prefix + '_SideWasher' + str(k), conv(washer_s), steel_col, offset)
            add(prefix + '_Side_M4x14_' + str(k), conv(screw_s), steel_col, offset)

# ==============================================================================
# 8B. FRONT & REAR TOP-RAIL L-BRACKETS, DROP-IN SQUARE NUT BARS & FASTENERS (FB0..1, BB0..1)
#     - Replicates S04 embedded nut bar inside front/rear top wood rail (Z=70..86)!
#     - Compact 16mm tall vertical leg (Z=70..86) completely clears the 48mm window (Z=21..69)!
# ==============================================================================
for back in [False, True]:
    for j, x in enumerate(front_nut_xs):
        prefix = ('BB' if back else 'FB') + str(j)
        conv = rear if back else (lambda s: s)
        offset = (0, 45 if back else -45, 25)

        f_bracket = box(24.0, 3.0, 16.0, x - 12.0, 20.0, 70.0).fuse(
            box(24.0, 28.0, 3.0, x - 12.0, 20.0, 83.0)
        ).removeSplitter()
        f_slot = (
            cyl(2.25, 5.0, x, 35.5, 82.0)
            .fuse(cyl(2.25, 5.0, x, 38.5, 82.0))
            .fuse(box(4.5, 3.0, 5.0, x - 2.25, 35.5, 82.0))
        )
        f_bracket = f_bracket.cut(f_slot)
        for dx in [-6.0, 6.0]:
            f_bracket = f_bracket.cut(cyl(2.25, 5.0, x + dx, 19.0, 75.5, (0, 1, 0)))
        add(prefix + '_Bracket', conv(f_bracket), steel_col, offset,
            '3mm Stainless/Aluminium Front/Rear Compact L-Bracket (Z=70..86)')

        washer_up = cyl(4.5, 1.0, x, 37.0, 82.0).cut(cyl(2.2, 1.0, x, 37.0, 82.0))
        screw_up = cyl(2.0, 8.0, x, 37.0, 82.0).fuse(cyl(3.5, 3.5, x, 37.0, 78.5))
        screw_up = screw_up.cut(cyl(1.5, 2.0, x, 37.0, 78.4))
        add(prefix + '_TopWasher', conv(washer_up), steel_col, (0, 0, -25))
        add(prefix + '_Up_M4x8', conv(screw_up), steel_col, (0, 0, -40))

        f_nut_bar = box(20.0, 4.0, 14.0, x - 10.0, 9.7, 71.0)
        for dx in [-6.0, 6.0]:
            f_nut_bar = f_nut_bar.cut(cyl(1.65, 4.2, x + dx, 9.6, 75.5, (0, 1, 0)))
        add(prefix + '_SquareNutBar', conv(f_nut_bar), brass_col, (0, 0, 35),
            'Drop-In Square Nut Bar 20x14x4 (M4x2) in front/rear top-step blind mortise (per S04)')

        for k, dx in enumerate([-6.0, 6.0]):
            washer_s = cyl(4.5, 1.0, x + dx, 23.0, 75.5, (0, 1, 0)).cut(
                cyl(2.2, 1.0, x + dx, 23.0, 75.5, (0, 1, 0))
            )
            screw_s = cyl(2.0, 14.0, x + dx, 10.0, 75.5, (0, 1, 0)).fuse(
                cyl(3.5, 3.0, x + dx, 24.0, 75.5, (0, 1, 0))
            )
            screw_s = screw_s.cut(cyl(1.5, 1.8, x + dx, 25.3, 75.5, (0, 1, 0)))
            add(prefix + '_SideWasher' + str(k), conv(washer_s), steel_col, offset)
            add(prefix + '_Side_M4x14_' + str(k), conv(screw_s), steel_col, offset)

# ==============================================================================
# 9. FRONT & REAR PANEL SCREWS + WASHERS (M3x20 through 16mm wood shoulder)
# ==============================================================================
for back in [False, True]:
    for i, (x, z) in enumerate(holes):
        washer = cyl(3.5, 1.0, x, T, z, (0, 1, 0)).cut(cyl(1.7, 1.0, x, T, z, (0, 1, 0)))
        screw = cyl(1.5, 20.0, x, T + 1.0 - 20.0, z, (0, 1, 0)).fuse(cyl(2.8, 2.2, x, T + 1.0, z, (0, 1, 0)))
        screw = screw.cut(cyl(1.1, 1.2, x, T + 2.1, z, (0, 1, 0)))
        for suffix, ss in [('Washer', washer), ('M3x20', screw)]:
            add(('R' if back else 'F') + '_%02d_' % i + suffix, rear(ss) if back else ss, steel_col,
                (0, 75 if back else -75, 0), 'M3x20 interior panel fastener')

# ==============================================================================
# 10. METADATA, EXPORT & RIGOROUS GEOMETRIC VALIDATION
# ==============================================================================
meta = doc.addObject('App::FeaturePython', 'Master_Dimensions')
for k, v in [
    ('Width', W), ('Depth', D), ('WoodHeight', H), ('WoodThickness', T),
    ('TopLowerHeight', TOP_LOWER_H), ('TopUpperHeight', TOP_UPPER_H),
    ('PanelWidth', PW), ('PanelHeight', PH), ('PanelThickness', PT),
    ('PanelRebateDepth', REBATE_DEPTH), ('PanelProtrusion', PANEL_PROTRUDE),
    ('WindowWidth', WIN_W), ('WindowHeight', WIN_H)
]:
    meta.addProperty('App::PropertyLength', k)
    setattr(meta, k, v)
meta.addProperty('App::PropertyString', 'Rebuild')
meta.Rebuild = 'Edit constants in cad/build_chassis_d05.py and rerun; metadata is not a live feature driver.'

doc.recompute()
doc.saveAs(str(OUT / 'CB002_D05.FCStd'))
Part.export(shapes, str(OUT / 'CB002_D05_assembly.step'))
for o in shapes[:15]:  # W01..W04, A01..A03, F01..F04, CB01..CB04
    Part.export([o], str(OUT / (o.Name + '.step')))
for o in shapes:
    if o.Name.endswith('_Bracket'):
        Part.export([o], str(OUT / (o.Name + '.step')))

(OUT / 'mesh_scene.json').write_text(json.dumps(parts))

# Validation 1: Non-fastener structural solids (Wood W01..W04, Plates A01..A03, Feet F01..F04, CornerBlocks CB01..04, Splines SP01..08, 10 Brackets)
struct = shapes[:23] + [o for o in shapes if o.Name.endswith('_Bracket')]
for i, a in enumerate(struct):
    for b in struct[i + 1:]:
        vol = a.Shape.common(b.Shape).Volume
        assert vol < 0.01, f"Structural interference: {a.Name} vs {b.Name} ({vol:.4f} mm^3)"

# Validation 2: Fasteners & square nuts must not intersect wood (W01..W04) or corner blocks (CB01..CB04)
for o in shapes:
    if (o.Name.startswith(('F_', 'R_')) or
            '_Side_M4' in o.Name or '_Up_M4' in o.Name or 'Washer' in o.Name or 'SquareNutBar' in o.Name):
        for w in shapes[:4] + shapes[11:15]:
            vol = o.Shape.common(w.Shape).Volume
            assert vol < 0.01, f"Fastener/Nut wood interference: {o.Name} vs {w.Name} ({vol:.4f} mm^3)"

# Validation 3: Straight Ø8mm screwdriver approach from open bottom to all 10 vertical M4x8 heads
for x, y in top_pts:
    tool = cyl(4.0, 78.4, x, y, -20.0)
    for o in struct:
        vol = tool.common(o.Shape).Volume
        assert vol < 0.01, f"Tool approach blocked by {o.Name} at ({x}, {y})"

# Validation 4: Top highest 0.5mm slab is completely solid (zero holes on top surface)
top_slab_z = H + TOP_LOWER_H + TOP_UPPER_H - 0.5
top_cap_w = W - 2 * (TOP_UPPER_INSET + 0.8)
top_cap_d = D - 2 * (TOP_UPPER_INSET + 0.8)
slab_box = box(top_cap_w, top_cap_d, 0.5, TOP_UPPER_INSET + 0.8, TOP_UPPER_INSET + 0.8, top_slab_z)
assert abs(top.common(slab_box).Volume - top_cap_w * top_cap_d * 0.5) < 0.01, "Top surface has holes!"

# Validation 5: Inner 404x48 wiring aperture is 100% clear through remaining 16mm wood (and brackets!), while 6 washer-bearing shoulders remain
window_check = rr_y(W / 2 - WIN_W / 2, H / 2 - WIN_H / 2, WIN_W, WIN_H, WIN_R, REBATE_DEPTH + 0.01, WOOD_SHOULDER_T + 5.0)
for o in struct:
    if not o.Name.startswith('A0'):
        assert o.Shape.common(window_check).Volume < 0.01, f"Inner wiring window blocked by {o.Name}!"
for x, z in holes:
    bearing = cyl(3.5, WOOD_SHOULDER_T - 0.02, x, REBATE_DEPTH + 0.01, z, (0, 1, 0)).cut(
        cyl(1.71, WOOD_SHOULDER_T - 0.02, x, REBATE_DEPTH + 0.01, z, (0, 1, 0))
    )
    assert abs(front.common(bearing).Volume - bearing.Volume) < 0.01, f"Missing wood shoulder at ({x}, {z})"

# Validation 6: STEP roundtrip readback check
roundtrip = Part.read(str(OUT / 'CB002_D05_assembly.step'))
assert len(roundtrip.Solids) == len(shapes) and roundtrip.isValid(), "STEP roundtrip failed!"

report = [
    'D05 high-fidelity concept validation — Burmese Teak + Black Walnut Splines + 10-Point All-Wall Square Nut Bars + Protruding Panels (CONCEPT — NOT FOR MANUFACTURE)',
    f'{len(shapes)} valid positive-volume solids; STEP readback verified ({len(roundtrip.Solids)} solids).',
    '45-deg mitered Burmese Teak rails, 8 Black Walnut corner splines (14x14x5), 4 internal corner glue blocks, protruding plates, feet and 10 L-brackets: zero volumetric interference.',
    '404x48 inner wiring aperture (+20% taller for ALPS RK50 & meters) is 100% clear through remaining 16mm wood; six full washer-bearing wood shoulders retained per frame.',
    'Front & rear 6mm panels recessed 4.0mm into wood rebate and protrude 2.0mm proud of wood face with perimeter chamfer.',
    '10 drop-in dual-M4 square nut bars (6 on Left/Right + 4 on Front/Rear top rails per S04) seated in top-rabbet blind mortises with 6.0mm solid wood shoulder and zero collision.',
    'Stepped two-tier top plate highest 0.5mm full slab verified: zero top-surface holes; wood top rim (Z=90) and bottom (Z=0) have zero exposed holes.',
    'Ten vertical Ø8mm tool approach cylinders from bottom clear wood/plates/brackets/feet/corner-blocks.',
    'Top M4x8 (10x): washer 1 + bracket 3 + blind thread engagement 4; drill-bottom margin > 6mm.',
    'Side & Front/Rear M4x14 (20x): washer 1 + bracket 3 + wood shoulder 6.0 + drop-in square nut bar engagement 4.',
    'Front/rear M3x20 (12x): washer 1 + wood shoulder 16 + panel blind engagement 3.',
    'All dimensions are [ASSUMED]/[TO VERIFY] drafts. No structural, thermal, electrical or manufacturing release.'
]
(OUT / 'validation.txt').write_text('\n'.join(report))

bom_lines = [
    'Part,Quantity,Description,Status',
    'W01-W02,2,Burmese Teak 520x20x90 with 45-deg miter + 2 spline slots + outer 444.6x64.6x4 rebate + inner 404x48 window + 2 top-rabbet nut mortises,ASSUMED',
    'W03-W04,2,Burmese Teak 20x380x90 with 45-deg miter + 2 spline slots + 3 top-rabbet drop-in square nut mortises,ASSUMED',
    'SP01-SP08,8,American Black Walnut corner spline (14x14x5mm right-triangle across 45-deg miter at Z=21..26 & Z=64..69),ASSUMED',
    'CB01-CB04,4,Burmese Teak internal corner reinforcement block 22x22x78mm (per S04 corner post),ASSUMED',
    'A01-A02,2,Chamfered Brass/Aluminium 444x64x6 R8 panel blanks (4mm recessed / 2mm proud of wood) with 6x M3 blind holes,ASSUMED',
    'A03,1,Two-tier stepped top plate 520x380 (lower 8 + upper 5 + boss 4) with 10-point hidden underside fixing,ASSUMED',
    'F01-F04,4,CNC machined gold foot Ø48x14 with chamfer and groove,ASSUMED',
    'LB0-RB2,6,3mm stainless/aluminium side internal L-bracket (24mm wide x 22mm tall),ASSUMED',
    'FB0-BB1,4,3mm stainless/aluminium front/rear compact internal L-bracket (24mm wide x 16mm tall above window),ASSUMED',
    'Side_SquareNutBar,6,Drop-in dual-M4 square nut bar 20x16x4 in left/right top-rabbet blind mortise,ASSUMED',
    'FrontRear_SquareNutBar,4,Drop-in dual-M4 square nut bar 20x14x4 in front/rear top-rabbet blind mortise (per S04),ASSUMED',
    'M3x20,12,Front/rear panel interior socket button head screws through 16mm wood shoulder,ASSUMED',
    'M3 washer,12,Ø7x1mm flat washer resting on 16mm wood shoulder,ASSUMED',
    'M4x8,10,Upward top-plate fixing socket head cap screws (6 side + 4 front/rear),ASSUMED',
    'M4x14,20,Horizontal bracket screws into drop-in square nut bars (12 side + 8 front/rear),ASSUMED',
    'M4 washer,30,Ø9x1mm flat washer,ASSUMED'
]
(OUT / 'BOM.csv').write_text('\n'.join(bom_lines) + '\n')
print('\n'.join(report))
