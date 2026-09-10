#!/usr/bin/env python3
"""Generate TB001 D06 Line & Plane: restrained Freddy Tuppen × Audo cues."""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tb001_three_tier as base  # noqa: E402
from tb001_d05 import chamfered_prism  # noqa: E402

OUT = ROOT / '02_Tables/TB001_D16_Three_Tier/models/D06'
P = json.loads((OUT / 'parameters.json').read_text())
base.OUT = OUT
base.P = P
base.REV = P['revision']
base.PARTS = []
base.COLORS = {'SAPELE': '#653f2c', 'OAK': '#bf9d70'}


def build():
    w, d, h = P['width'], P['depth'], P['height']
    s, px, py = P['setback'], P['post_x'], P['post_y']
    core, edge = P['leg_core_x'], P['leg_edge_x']
    xs, ys = [s, w-s-px], [s, d-s-py]
    leg_h = h-P['top_thickness']

    # Wide oak blades carry one dark sapele edge only. This keeps Freddy
    # Tuppen's overlaid line language without returning to D04's repeated grid.
    for side, x in enumerate(xs):
        for front, y in enumerate(ys):
            if side == 0:
                base.box(f'Oak blade leg {side+1}{front+1}', 'Legs', 'OAK',
                         x+edge, y, 0, core, py, leg_h)
                base.box(f'Sapele outer edge {side+1}{front+1}', 'Leg lines', 'SAPELE',
                         x, y, 0, edge, py, leg_h)
            else:
                base.box(f'Oak blade leg {side+1}{front+1}', 'Legs', 'OAK',
                         x, y, 0, core, py, leg_h)
                base.box(f'Sapele outer edge {side+1}{front+1}', 'Leg lines', 'SAPELE',
                         x+core, y, 0, edge, py, leg_h)

    inner_x, inner_y = s+px, s+py
    inner_w, inner_d = w-2*(s+px), d-2*(s+py)
    line_d = P['shelf_line_depth']
    for label, level in zip(['Lower', 'Middle'], P['surface_levels'][:2]):
        # A light plane plus only two dark transverse lines.
        chamfered_prism(f'{label} oak plane', label, 'OAK',
                        inner_x+2, inner_y+line_d, level-P['shelf_panel_thickness'],
                        inner_w-4, inner_d-2*line_d, P['shelf_panel_thickness'],
                        P['shelf_chamfer'])
        for y in [inner_y, inner_y+inner_d-line_d]:
            base.box(f'{label} sapele line', label, 'SAPELE',
                     inner_x-P['panel_extension'], y, level-P['shelf_frame_thickness'],
                     inner_w+2*P['panel_extension'], line_d, P['shelf_frame_thickness'])

    # One deliberate rear line establishes orientation and resists visual symmetry.
    back_y = ys[1] + (py-P['back_stretcher_depth'])/2
    base.box('Single rear stretcher', 'Structure', 'SAPELE',
             xs[0]+px, back_y, P['back_stretcher_z'], xs[1]-xs[0]-px,
             P['back_stretcher_depth'], P['back_stretcher_height'])

    # Audo-like simple silhouette: broad overhanging top, one material contrast.
    rail = P['top_rail_width']
    projection = P['top_projection']
    for y in [0, d-rail]:
        base.box('Top projecting sapele line', 'Top', 'SAPELE',
                 -projection, y, leg_h, w+2*projection, rail, P['top_thickness'])
    for x in [0, w-rail]:
        base.box('Top side sapele line', 'Top', 'SAPELE',
                 x, rail, leg_h, rail, d-2*rail, P['top_thickness'])
    chamfered_prism('Top oak plane', 'Top', 'OAK', rail+2, rail+2,
                    h-P['top_panel_thickness'], w-2*(rail+2), d-2*(rail+2),
                    P['top_panel_thickness'], P['top_chamfer'])

    a, at = P['apron_height'], P['apron_thickness']
    for y in ys:
        base.box('Quiet front/back apron', 'Top', 'SAPELE', xs[0]+px,
                 y+(py-at)/2, leg_h-a, xs[1]-xs[0]-px, at, a)


def verify():
    checks = base.verify()
    checks.update(
        concept='Line & Plane — restrained Freddy Tuppen × Audo',
        note=('D06 uses broad oak blade legs with one sapele edge, two transverse lines per shelf, '
              'a single rear stretcher and a quiet overhanging top. Exterior concept only; '
              'joinery, racking resistance and wood movement remain unverified.'),
    )
    return checks


def write_viewer(data):
    template = (ROOT/'scripts/tb001_viewer.html').read_text()
    html = template.replace('__DATA__', json.dumps(data, separators=(',', ':')))
    replacements = {
        '<title>TB001 · D16 三層邊几</title>': '<title>TB001 D06 · Line & Plane 三層邊几</title>',
        'TB001 / D04 · D16 DESIGN FAMILY': 'TB001 / D06 · LINE & PLANE',
        'D16 三層邊几 · 貼地底層': 'Line & Plane 三層邊几',
        '底層離地降為6 cm，移除底板下橫飾條。保留三明治腳、胡桃木腳墊與出頭橫條。':
            'Freddy Tuppen 的疊線與雙材質語彙，經 Audo 式簡化後只保留必要的水平線。',
        '含出頭最大尺寸 · 寬 × 深 × 高': '含桌緣出頭 · 寬 × 深 × 高',
        '64 × 48 × 60 cm': '62 × 48 × 60 cm',
        '主面板寬 60 cm；橫條左右各伸出 2 cm。<br>腳：胡桃木 8／楓木 14／胡桃木 8 mm。':
            '白橡木寬板腿＋單側沙比利木線。<br>視覺模型不是開料尺寸。',
        '#63432e"></span>胡桃木框與角條': '#653f2c"></span>沙比利木線與桌框',
        '#d9bd89"></span>楓木面板與腳身': '#bf9d70"></span>自然白橡木面與寬板腿',
        '中層離地 35 cm<br>下層離地 6 cm': '中層離地 33.6 cm<br>下層離地 8.8 cm',
        'TB001_D04.glb': 'TB001_D06.glb',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    html = html.replace(
        '<details><summary>查看立體與三視圖尺寸板</summary>',
        '<details open><summary>AI 木紋與材質效果（非尺寸依據）</summary>'
        '<img src="gallery/persp_ai.png" alt="D06 白橡木與沙比利木 AI 材質效果">'
        '<p>此圖只用於材質、光線與整體氣氛判斷；幾何與尺寸以互動模型及 CAD 預覽為準。</p>'
        '</details><details><summary>查看立體與三視圖尺寸板</summary>'
    )
    (OUT/'TB001_D06_viewer.html').write_text(html)


def customize_svg():
    base.svg()
    path = OUT/'preview.svg'
    content = path.read_text()
    replacements = {
        'THROUGH LINES': 'LINE &amp; PLANE',
        'D16 三層邊几': 'Line &amp; Plane 三層邊几',
        '01 / 三層 · D16 的雙色框架': '01 / Freddy Tuppen × Audo',
        '胡桃木框 × 楓木面': '沙比利木線 × 白橡木面',
        '8 / 14 / 8 mm 三明治腳': '寬板腿 · 單側 8 mm 深色線',
        '橫桿出頭 20 mm · 純楓木面': '每層只留兩道橫向線',
        '寬深按使用者公分需求換算；高度、層位及截面為本輪設計。榫接、面板托持及實木活動量待工程化。':
            'D06 概念：保留疊線與雙材質，但減少重複格柵。接合、抗搖與實木活動量仍待工程化。',
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    path.write_text(content)


def main():
    build()
    checks = verify()
    data = dict(revision=P['revision'], units='mm', parameters=P, parts=base.PARTS)
    (OUT/'geometry_mm.json').write_text(json.dumps(data, separators=(',', ':')))
    with (OUT/'parts_dimensions.csv').open('w', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(['id','name','group','material','x_mm','y_mm','z_mm',
                         'width_mm','depth_mm','height_mm','status'])
        for part in base.PARTS:
            writer.writerow([part['id'],part['name'],part['group'],part['material'],
                             *part['origin_mm'],*part['size_mm'],'CONCEPT exterior, not cut list'])
    base.glb()
    customize_svg()
    write_viewer(data)
    (OUT/'model_checks.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False))
    print(json.dumps(checks, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
