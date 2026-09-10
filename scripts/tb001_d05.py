#!/usr/bin/env python3
"""Generate TB001 D05 Quiet Frame concept from the shared TB001 exporters."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tb001_three_tier as base  # noqa: E402

OUT = ROOT / '02_Tables/TB001_D16_Three_Tier/models/D05'
P = json.loads((OUT / 'parameters.json').read_text())

base.OUT = OUT
base.P = P
base.REV = P['revision']
base.PARTS = []
base.COLORS = {'SMOKED_OAK': '#594638', 'NATURAL_OAK': '#c8aa7d'}


def poly_prism(name, group, material, points, z, height):
    """Add a vertical prism whose plan is a counter-clockwise polygon."""
    n = len(points)
    vertices = [[x, y, z] for x, y in points] + [[x, y, z + height] for x, y in points]
    faces = [list(reversed(range(n))), list(range(n, 2 * n))]
    faces += [[i, (i + 1) % n, (i + 1) % n + n, i + n] for i in range(n)]
    xs, ys = zip(*points)
    base.PARTS.append(dict(
        id=f'P{len(base.PARTS)+1:03}', name=name, group=group, material=material,
        origin_mm=[min(xs), min(ys), z],
        size_mm=[max(xs) - min(xs), max(ys) - min(ys), height],
        vertices_mm=vertices, faces=faces,
    ))


def chamfered_prism(name, group, material, x, y, z, width, depth, height, chamfer):
    points = [
        (x + chamfer, y), (x + width - chamfer, y),
        (x + width, y + chamfer), (x + width, y + depth - chamfer),
        (x + width - chamfer, y + depth), (x + chamfer, y + depth),
        (x, y + depth - chamfer), (x, y + chamfer),
    ]
    poly_prism(name, group, material, points, z, height)


def tapered_leg(name, x, y, z, height):
    tx, ty = P['post_x'], P['post_y']
    bx, by = P['post_bottom_x'], P['post_bottom_y']
    dx, dy = (tx - bx) / 2, (ty - by) / 2
    bottom = [(x + dx, y + dy), (x + dx + bx, y + dy),
              (x + dx + bx, y + dy + by), (x + dx, y + dy + by)]
    top = [(x, y), (x + tx, y), (x + tx, y + ty), (x, y + ty)]
    vertices = [[px, py, z] for px, py in bottom] + [[px, py, z + height] for px, py in top]
    faces = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4],
             [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    base.PARTS.append(dict(
        id=f'P{len(base.PARTS)+1:03}', name=name, group='Legs', material='SMOKED_OAK',
        origin_mm=[x, y, z], size_mm=[tx, ty, height], vertices_mm=vertices, faces=faces,
    ))


def build():
    w, d, h = P['width'], P['depth'], P['height']
    sx, sy, s = P['post_x'], P['post_y'], P['setback']
    leg_height = h - P['top_thickness']
    xs = [s, w - s - sx]
    ys = [s, d - s - sy]
    for ix, x in enumerate(xs):
        for iy, y in enumerate(ys):
            tapered_leg(f'Tapered leg {ix + 1}{iy + 1}', x, y, 0, leg_height)

    # Quiet tray shelves span only between the legs: one base and one inset panel,
    # with no repeated side bars or projecting crosspieces.
    inner_x, inner_y = s + sx, s + sy
    inner_w = w - 2 * s - 2 * sx
    inner_d = d - 2 * s - 2 * sy
    for label, level in zip(['Lower', 'Middle'], P['surface_levels'][:2]):
        total = P['shelf_frame_thickness']
        chamfered_prism(
            f'{label} smoked-oak tray base', label, 'SMOKED_OAK',
            inner_x, inner_y, level - total, inner_w, inner_d,
            P['shelf_base_thickness'], P['shelf_chamfer'],
        )
        inset = P['shelf_inset']
        chamfered_prism(
            f'{label} natural-oak inset', label, 'NATURAL_OAK',
            inner_x + inset, inner_y + inset, level - P['shelf_insert_thickness'],
            inner_w - 2 * inset, inner_d - 2 * inset,
            P['shelf_insert_thickness'], max(6, P['shelf_chamfer'] - 4),
        )

    # One rear stretcher replaces the eight decorative through-lines in D04.
    back_y = ys[1] + (sy - P['back_stretcher_depth']) / 2
    base.box(
        'Single rear stretcher', 'Structure', 'SMOKED_OAK',
        xs[0] + sx, back_y, P['back_stretcher_z'],
        xs[1] - xs[0] - sx, P['back_stretcher_depth'], P['back_stretcher_height'],
    )

    # Compact aprons provide a visually quiet transition into the top.
    a, at = P['apron_height'], P['apron_thickness']
    for y in ys:
        base.box('Front/back apron', 'Top', 'SMOKED_OAK', xs[0] + sx, y + (sy-at)/2,
                 leg_height-a, xs[1]-xs[0]-sx, at, a)
    for x in xs:
        base.box('Side apron', 'Top', 'SMOKED_OAK', x + (sx-at)/2, ys[0] + sy,
                 leg_height-a, at, ys[1]-ys[0]-sy, a)

    chamfered_prism('Smoked-oak top base', 'Top', 'SMOKED_OAK', 0, 0, leg_height,
                    w, d, P['top_base_thickness'], P['top_chamfer'])
    inset = P['top_inset']
    chamfered_prism('Natural-oak top inset', 'Top', 'NATURAL_OAK', inset, inset,
                    leg_height + P['top_base_thickness'], w-2*inset, d-2*inset,
                    P['top_insert_thickness'], P['top_chamfer']-6)


def verify():
    checks = base.verify()
    checks.update(
        clear_opening_front_mm=[228, 214],
        concept='Quiet Frame — Japandi with Danish/French restraint',
        note=('D05 removes D04 sandwich legs, projecting bars and split panels. '
              'Tapered solid legs, chamfered tray planes and one rear stretcher are exterior concepts; '
              'joinery, racking resistance and solid-wood movement remain unverified.'),
    )
    return checks


def customize_svg():
    base.svg()
    path = OUT / 'preview.svg'
    content = path.read_text()
    replacements = {
        'THROUGH LINES': 'QUIET FRAME',
        'D16 三層邊几': 'Quiet Frame 三層邊几',
        '01 / 三層 · D16 的雙色框架': '01 / Japandi × 歐陸木作',
        '胡桃木框 × 楓木面': '煙燻橡木 × 自然橡木',
        '8 / 14 / 8 mm 三明治腳': '單體錐形腳 · 上 34 × 38 mm',
        '橫桿出頭 20 mm · 純楓木面': '圓角托盤面 · 單一道後撐',
        '寬深按使用者公分需求換算；高度、層位及截面為本輪設計。榫接、面板托持及實木活動量待工程化。':
            'D05 概念：刪除重複格柵與出頭，改用錐形實木腿、柔角托盤面及單一道後撐。結構仍待工程化。',
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    path.write_text(content)


def main():
    build()
    checks = verify()
    data = dict(revision=P['revision'], units='mm', parameters=P, parts=base.PARTS)
    (OUT / 'geometry_mm.json').write_text(json.dumps(data, separators=(',', ':')))

    import csv
    with (OUT / 'parts_dimensions.csv').open('w', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(['id','name','group','material','x_mm','y_mm','z_mm',
                         'width_mm','depth_mm','height_mm','status'])
        for part in base.PARTS:
            writer.writerow([part['id'], part['name'], part['group'], part['material'],
                             *part['origin_mm'], *part['size_mm'],
                             'CONCEPT exterior, not cut list'])

    base.glb()
    customize_svg()
    template = (ROOT / 'scripts/tb001_viewer.html').read_text()
    (OUT / 'TB001_D05_viewer.html').write_text(
        template.replace('__DATA__', json.dumps(data, separators=(',', ':')))
        .replace('<title>TB001 · D16 三層邊几</title>', '<title>TB001 D05 · Quiet Frame 三層邊几</title>')
        .replace('TB001 / D04 · D16 DESIGN FAMILY', 'TB001 / D05 · QUIET FRAME')
        .replace('D16 三層邊几 · 貼地底層', 'Quiet Frame 三層邊几')
        .replace('底層離地降為6 cm，移除底板下橫飾條。保留三明治腳、胡桃木腳墊與出頭橫條。',
                 '降低線條密度，以錐形單體腿、柔角托盤面及單一道後撐建立偏歐美的 Japandi。')
        .replace('含出頭最大尺寸 · 寬 × 深 × 高', '外廓尺寸 · 寬 × 深 × 高')
        .replace('64 × 48 × 60 cm', '60 × 48 × 60 cm')
        .replace('主面板寬 60 cm；橫條左右各伸出 2 cm。<br>腳：胡桃木 8／楓木 14／胡桃木 8 mm。',
                 '煙燻橡木單體錐形腿；自然橡木嵌面。<br>視覺模型不是開料尺寸。')
        .replace('#63432e"></span>胡桃木框與角條', '#594638"></span>煙燻橡木框架')
        .replace('#d9bd89"></span>楓木面板與腳身', '#c8aa7d"></span>自然橡木嵌面')
        .replace('中層離地 35 cm<br>下層離地 6 cm', '中層離地 33.8 cm<br>下層離地 9.2 cm')
        .replace('TB001_D04.glb', 'TB001_D05.glb')
    )
    (OUT / 'model_checks.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False))
    print(json.dumps(checks, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
