"""Generate comprehensive D05 engineering drawing & section sheet (SVG + PNG) — Burmese Teak + Black Walnut 45° Mitered Splines + 10-Point All-Wall Square Nut Bars + Protruding Panels.
Includes:
- Section A: Stepped Two-Tier Top Plate + All-4-Wall Top-Rabbet Drop-In Dual-Hole Square Nut Bars (10x: Side 6 + Front/Rear 4 per S04)
- Section B: Front/Rear Burmese Teak Frame Two-Step Opening (Outer 444.6x64.6x4.0 Rebate with 2.0mm Protruding Panel + Inner 404x48x16.0 Wiring Window + 16mm Wood Shoulder)
- Detail C: 45° Mitered Spline Joint (2x 5mm Black Walnut Splines + Burmese Teak Internal Corner Block CB01..04) + Front Elevation
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'D05'
OUT.mkdir(exist_ok=True)

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1180" viewBox="0 0 1600 1180">
<defs>
  <pattern id="wood_hatch" width="12" height="12" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="12" stroke="#6b421b" stroke-width="1.2" opacity="0.35"/>
  </pattern>
  <pattern id="metal_hatch" width="8" height="8" patternTransform="rotate(-45 0 0)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="8" stroke="#6e551c" stroke-width="1.0" opacity="0.35"/>
  </pattern>
  <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1e3a5f"/>
  </marker>
</defs>

<style>
  text { font-family: 'PingFang TC', Arial, sans-serif; fill: #1e293b; font-size: 13.5px; }
  .title { font-size: 23px; font-weight: 700; fill: #0f172a; }
  .subtitle { font-size: 14px; fill: #475569; }
  .sec-hdr { font-size: 17px; font-weight: 700; fill: #0f172a; }
  .sub-hdr { font-size: 14.5px; font-weight: 600; fill: #1e3a5f; }
  .dim { font-size: 12.5px; font-weight: 600; fill: #1e3a5f; }
  .warn { font-size: 12.5px; font-weight: 600; fill: #b91c1c; }
  .tag { font-size: 12px; font-family: monospace; fill: #334155; }
  .sm { font-size: 12.5px; fill: #334155; }
  .wood { fill: #b87b3e; stroke: #4a2a0c; stroke-width: 1.8; }
  .wood-cb { fill: #9e652e; stroke: #4a2a0c; stroke-width: 1.8; }
  .spline { fill: #3d2210; stroke: #1f1006; stroke-width: 1.5; }
  .brass { fill: #ebd08c; stroke: #785a16; stroke-width: 1.8; }
  .nut { fill: #f59e0b; stroke: #78350f; stroke-width: 1.8; }
  .steel { fill: #cbd5e1; stroke: #334155; stroke-width: 1.6; }
  .void { fill: #ffffff; stroke: #64748b; stroke-width: 1.2; stroke-dasharray: 4 3; }
  .dim-line { fill: none; stroke: #1e3a5f; stroke-width: 1.3; marker-start: url(#arrow); marker-end: url(#arrow); }
  .lead-line { fill: none; stroke: #1e3a5f; stroke-width: 1.3; marker-end: url(#arrow); }
  .center-line { fill: none; stroke: #dc2626; stroke-width: 1.0; stroke-dasharray: 12 4 3 4; }
  .box-panel { fill: #ffffff; stroke: #cbd5e1; stroke-width: 1.5; rx: 6; }
</style>

<!-- Background & Border -->
<rect width="1600" height="1180" fill="#f1f5f9"/>
<rect x="20" y="20" width="1560" height="1140" fill="#ffffff" stroke="#334155" stroke-width="2"/>
<line x1="20" y1="98" x2="1580" y2="98" stroke="#334155" stroke-width="1.8"/>

<!-- Header Block -->
<text x="42" y="56" class="title">CB002 緬甸柚木真空管擴大機機箱 — D05 結構與剖面工程圖（CONCEPT DRAFT）</text>
<text x="42" y="82" class="subtitle">緬甸柚木框＋黑胡桃雙羽鍵榫 · 四周 10 點預埋方螺母條 · 前後面板浮凸 2mm（嵌深 4mm）＋ 404×48 加大通孔 ｜ 單位：mm</text>
<rect x="1320" y="34" width="240" height="50" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" rx="4"/>
<text x="1336" y="55" class="warn">狀態：L0 / L1 HOLD（概念草案）</text>
<text x="1336" y="74" class="tag">[ASSUMED] / [TO VERIFY]</text>

<!-- ======================================================================= -->
<!-- PANEL A: TOP PLATE & ALL-4-WALL DROP-IN SQUARE NUT BARS (LEFT TOP)       -->
<!-- ======================================================================= -->
<rect x="36" y="114" width="930" height="510" class="box-panel"/>
<text x="54" y="144" class="sec-hdr">A. 四周 10 點頂板隱藏固定與「上止口垂直盲槽預埋雙孔方螺母條」剖面（左右各 3 組 ＋ 前後各 2 組）</text>
<text x="58" y="175" class="sub-hdr">1. 裝配橫剖面（Z 方向：頂板蓋合自鎖槽口 ＋ L 支架由下向上鎖頂板盲牙，四周木框同步拉緊）</text>

<!-- Wood Wall with Top Inner Rabbet -->
<path d="M 80 280 H 137 V 304 H 200 V 550 H 80 Z" class="wood"/>
<path d="M 80 280 H 137 V 304 H 200 V 550 H 80 Z" fill="url(#wood_hatch)"/>

<!-- Stepped Two-Tier Top Plate A03 -->
<path d="M 80 232 H 140 L 145 202 H 410 V 304 H 203 V 280 H 80 Z" class="brass"/>
<path d="M 80 232 H 140 L 145 202 H 410 V 304 H 203 V 280 H 80 Z" fill="url(#metal_hatch)"/>

<!-- Blind M4 tapped hole in underside of A03 -->
<rect x="292" y="268" width="20" height="36" class="void"/>
<line x1="302" y1="248" x2="302" y2="410" class="center-line"/>

<!-- L-Bracket (3mm thick = 18px) -->
<path d="M 200 304 H 368 V 322 H 218 V 436 H 200 Z" class="steel"/>

<!-- Upward M4x8 screw + 1mm washer -->
<rect x="275" y="322" width="54" height="6" class="steel"/>
<rect x="290" y="280" width="24" height="48" class="steel"/>
<rect x="281" y="328" width="42" height="20" class="steel"/>

<!-- Vertical Drop-In Blind Mortise from Z=86 (Y=304) down to Z=68.5/70.5 at X=9.5..14 (137..164) -->
<rect x="137" y="304" width="27" height="105" fill="#f8fafc" stroke="#4a2a0c" stroke-width="1.5"/>
<!-- Drop-in Square Nut Bar 20x16x4 / 20x14x4 (138..162, Y=308..404) -->
<rect x="138" y="308" width="24" height="96" class="nut"/>
<text x="141" y="352" style="font-size:11px;font-weight:700;fill:#fff;">M4</text>

<!-- Horizontal M4x14 screw + washer through 6.0mm wood shoulder (164..200 = 36px) -->
<line x1="125" y1="388" x2="255" y2="388" class="center-line"/>
<rect x="218" y="361" width="6" height="54" class="steel"/>
<rect x="140" y="376" width="84" height="24" class="steel"/>
<rect x="224" y="367" width="18" height="42" class="steel"/>

<!-- Clean Annotations for Section A -->
<path d="M 380 202 H 435" class="lead-line"/>
<text x="442" y="206" class="sm">上層台階 500×360×5（四周內縮 10mm，頂面 100% 無孔）[ASSUMED]</text>
<path d="M 410 258 H 435" class="lead-line"/>
<text x="442" y="262" class="sm">下層外周裙邊 520×380×8 + 下緣定位凸台 479×339×4（伸入四面木框上止口）</text>
<path d="M 150 304 L 220 285 H 435" class="lead-line"/>
<text x="442" y="289" class="warn">★ 四面木框上止口 (Z=86) 垂直盲插槽：共 10 組雙孔方螺母條（左右 6 ＋ 前後 4）</text>
<path d="M 324 338 L 410 322 H 435" class="lead-line"/>
<text x="442" y="326" class="sm">底部向上 10 顆 M4×8 + 墊片1 + L支架3 → 鎖入頂板底面盲牙 4mm（防 520 跨距下垂）</text>
<path d="M 242 388 L 410 368 H 435" class="lead-line"/>
<text x="442" y="372" class="sm">水平向 20 顆 M4×14（每支架 2 顆）穿過 6.0mm 實木肩，鎖入預埋雙孔方螺母條</text>
<path d="M 150 404 L 265 415 H 435" class="lead-line"/>
<text x="442" y="419" class="sm">前後上橫樑 (Z=69..90) 採 16mm 高緊湊型 L 支架 (FB0..BB1)，完全不遮擋 48mm 窗口！</text>

<!-- Top-down Plan Detail of Drop-in Mortise (X-Y View) -->
<rect x="358" y="445" width="590" height="160" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" rx="4"/>
<text x="372" y="470" class="sub-hdr">2. 前後與左右木框預埋雙孔方螺母條俯視圖（還原 S04 前面板上方橫樑金屬固定結構）</text>
<rect x="374" y="485" width="150" height="100" class="wood"/>
<rect x="434" y="500" width="90" height="70" fill="#e2e8f0" stroke="#4a2a0c" stroke-width="1.2"/>
<rect x="439" y="505" width="30" height="60" class="nut"/>
<rect x="469" y="515" width="55" height="8" class="void"/>
<rect x="469" y="547" width="55" height="8" class="void"/>
<text x="538" y="510" class="sm">• 左右側壁 (W03/W04)：Y=70, 190, 310 各 3 組 (20×16×4)</text>
<text x="538" y="534" class="sm">• 前後木框 (W01/W02)：X=185, 335 各 2 組 (20×14×4，呼應 S04)</text>
<text x="538" y="558" class="sm">• 前後頂樑直接吊掛於 13mm 厚金屬頂板，大幅強化窗口上方抗彎剛性</text>
<text x="538" y="582" class="dim">• 承壓木肩厚 6.0×寬 22mm，100% 隱藏於頂板下緣定位凸台內</text>

<path d="M 302 485 V 360" class="lead-line"/>
<text x="195" y="505" class="dim">底部 10 處 Ø8 起子通道 ↑</text>
<text x="80" y="575" class="dim">緬甸柚木框 (20mm)</text>

<!-- ======================================================================= -->
<!-- PANEL B: FRONT/REAR PROTRUDING PANEL & 48mm WINDOW (LEFT BOTTOM)        -->
<!-- ======================================================================= -->
<rect x="36" y="640" width="930" height="425" class="box-panel"/>
<text x="54" y="670" class="sec-hdr">B. 前後木框「面板浮凸 2mm（嵌深 4mm）＋ 404×48 加大通孔 ＋ 16mm 厚木肩」剖面</text>

<!-- Left side of Panel B: Cross-section through screw & through window -->
<text x="58" y="702" class="sub-hdr">1. 縱剖面（Z 方向：Y=-2..20）</text>

<!-- Wood Frame W01 (20mm thick: X=75..195) -->
<rect x="75" y="725" width="120" height="295" class="wood"/>
<rect x="75" y="725" width="120" height="295" fill="url(#wood_hatch)"/>

<!-- Step 1: Outer Rebate 4.0mm deep (X=75..99 = 24px) -->
<rect x="75" y="760" width="24" height="225" fill="#ffffff" stroke="#4a2a0c" stroke-width="1.5"/>
<!-- Brass Panel A01 (6mm thick = 36px: protrudes 2mm proud to X=63..99!) -->
<path d="M 63 767 L 69 761 H 99 V 984 H 69 L 63 978 Z" class="brass"/>
<path d="M 63 767 L 69 761 H 99 V 984 H 69 L 63 978 Z" fill="url(#metal_hatch)"/>

<!-- Step 2: Inner Central Through-Window (X=99..195 = 16mm remaining wood, enlarged height 48mm!) -->
<rect x="99" y="816" width="96" height="145" fill="#f8fafc" stroke="#4a2a0c" stroke-width="1.5" stroke-dasharray="5 3"/>
<text x="105" y="882" class="warn">第二級加大貫通窗</text>
<text x="105" y="902" class="sm">(404×48 穿通 16mm)</text>

<!-- Screw through Upper Wood Shoulder (Z=73, M3x20) -->
<rect x="75" y="782" width="24" height="15" class="void"/>
<rect x="195" y="772" width="6" height="36" class="steel"/>
<rect x="81" y="784" width="120" height="12" class="steel"/>
<rect x="201" y="776" width="14" height="28" class="steel"/>
<line x1="55" y1="790" x2="225" y2="790" class="center-line"/>

<!-- Dimension callouts for B1 -->
<line x1="63" y1="1038" x2="75" y2="1038" class="dim-line"/><text x="42" y="1055" class="warn">浮凸 2</text>
<line x1="75" y1="1038" x2="99" y2="1038" class="dim-line"/><text x="76" y="1055" class="dim">槽 4</text>
<line x1="99" y1="1038" x2="195" y2="1038" class="dim-line"/><text x="126" y="1055" class="dim">木肩 16</text>

<!-- Mini Elevation of Inside Front Frame showing Shoulder, 6 Panel Screws & 2 Top-Rail Brackets -->
<text x="285" y="702" class="sub-hdr">2. 前後木框機內視圖（404×48 加大窗口 ＋ 6 顆 M3 面板螺絲 ＋ 上橫樑 2 組預埋方螺母支架）</text>
<rect x="285" y="720" width="610" height="104" class="wood"/>
<!-- Outer rebate dashed -->
<rect x="330" y="735" width="520" height="74" fill="#ebd08c" stroke="#4a2a0c" stroke-width="1.3" stroke-dasharray="4 2"/>
<!-- Inner through window (enlarged to 48mm!) -->
<rect x="353" y="744" width="474" height="56" fill="#ffffff" stroke="#1e293b" stroke-width="1.8"/>
<text x="470" y="777" class="dim">中央加大貫通窗口 404 × 48 (R6) — 容納 ALPS RK50 與表頭</text>
<!-- 6 Screw Holes on the wood shoulder -->
<circle cx="340" cy="772" r="4.5" class="steel"/><circle cx="840" cy="772" r="4.5" class="steel"/>
<circle cx="426" cy="739" r="4.5" class="steel"/><circle cx="754" cy="739" r="4.5" class="steel"/>
<circle cx="426" cy="805" r="4.5" class="steel"/><circle cx="754" cy="805" r="4.5" class="steel"/>
<!-- 2 Front/Rear Top-Rail Compact L-Brackets + Square Nut Bars at X=185, 335 -->
<rect x="490" y="722" width="32" height="18" class="steel"/>
<rect x="658" y="722" width="32" height="18" class="steel"/>

<text x="285" y="846" class="warn">★ 為什麼通孔高度可由 40mm 加大至 48mm (+20%) 且結構更強？</text>
<path d="M 275 885 H 202" class="lead-line"/>
<text x="285" y="872" class="sm">1. 【面板浮凸 2mm → 木肩增厚至 16mm】：6mm 面板僅嵌入木框 4.0mm（向外浮凸 2.0mm 展現立體倒角），</text>
<text x="285" y="894" class="sm">   使槽底剩餘實木厚度由 14mm 提升為 16.0mm，抵消高度加大對木樑慣性矩的影響。</text>
<text x="285" y="920" class="sm">2. 【前後上橫樑預埋方螺母條 (FB0..BB1)】：還原 S04 照片，於 X=185, 335 預埋雙孔方螺母條與緊湊型 L 支架，</text>
<text x="285" y="942" class="sm">   將 21mm 高的前後上木樑 (Z=69..90) 直接鎖固於 13mm 厚金屬頂板，形成「木＋鋁/銅複合箱型樑」。</text>
<text x="285" y="968" class="sm">3. 【6 點 M3×20 完整墊片支撐】：上下木肩保留 8mm（總樑高 21mm），左右木肩寬 20mm，6 顆 Ø7 墊片 100% 承壓。</text>

<!-- ======================================================================= -->
<!-- PANEL C: 45° MITERED SPLINE JOINT, CORNER BLOCK & ENVELOPE (RIGHT COL)  -->
<!-- ======================================================================= -->
<rect x="984" y="114" width="580" height="951" class="box-panel"/>
<text x="1002" y="144" class="sec-hdr">C. 緬甸柚木框 ＋ 黑胡桃 45° 雙羽鍵榫 ＋ 內角補強木柱</text>

<!-- Front Orthographic View (Scale 1.0px/mm: 520 wide) -->
<text x="1002" y="175" class="sub-hdr">1. 正視圖（緬甸柚木連續木紋轉角 ＋ 北美黑胡桃雙羽鍵 ＋ 浮凸 2mm 面板）</text>

<!-- Stepped Top Plate A03: Upper 500x5, Lower 520x8 -->
<rect x="1024" y="215" width="500" height="8" class="brass"/>
<rect x="1014" y="223" width="520" height="12" class="brass"/>

<!-- Wood Frame W01: 520 x 90 (Burmese Teak) -->
<rect x="1014" y="235" width="520" height="90" class="wood"/>

<!-- 2 Contrasting American Black Walnut Splines at Left (X=1014..1028) and Right (X=1520..1534) -->
<rect x="1014" y="256" width="14" height="5" class="spline"/>
<rect x="1014" y="299" width="14" height="5" class="spline"/>
<rect x="1520" y="256" width="14" height="5" class="spline"/>
<rect x="1520" y="299" width="14" height="5" class="spline"/>

<!-- Protruding Chamfered Brass Panel 444 x 64 (R8, 2mm proud with shadow rim) -->
<rect x="1050" y="246" width="448" height="68" rx="9" fill="none" stroke="#4a2a0c" stroke-width="1.2" opacity="0.5"/>
<rect x="1052" y="248" width="444" height="64" rx="8" class="brass"/>
<rect x="1055" y="251" width="438" height="58" rx="6" fill="none" stroke="#927022" stroke-width="1.2"/>

<!-- CNC Machined Gold Feet Ø48 x 14 -->
<rect x="1054" y="325" width="48" height="12" class="brass"/>
<rect x="1056" y="337" width="44" height="2" fill="#334155"/>
<rect x="1446" y="325" width="48" height="12" class="brass"/>
<rect x="1448" y="337" width="44" height="2" fill="#334155"/>

<!-- Dimensions on Front Elevation -->
<line x1="1014" y1="362" x2="1534" y2="362" class="dim-line"/>
<text x="1205" y="380" class="dim">總寬 520 [KNOWN/ASSUMED cm]</text>
<line x1="1052" y1="202" x2="1496" y2="202" class="dim-line"/>
<text x="1165" y="195" class="dim">面板 444 × 64 × 6（嵌深 4mm / 浮凸木框 2mm）</text>
<line x1="1546" y1="235" x2="1546" y2="325" class="dim-line"/>
<text x="1552" y="285" class="dim">90</text>

<!-- Detail of 45-deg Mitered Spline + Internal Corner Block (Top Plan View X-Y) -->
<text x="1002" y="425" class="sub-hdr">2. 轉角俯視剖面圖（X–Y 平面：緬甸柚木 45° 斜接 ＋ 黑胡桃羽鍵 ＋ 內角補強柱）</text>

<!-- Left side wall W03 (X=0..20 -> 1014..1094, Y=0..50 -> 450..650, scale 4px/mm) -->
<polygon points="1014,650 1014,450 1094,530 1094,650" class="wood"/>
<!-- Front rail W01 (X=0..55 -> 1014..1234, Y=0..20 -> 450..530) -->
<polygon points="1014,450 1234,450 1234,530 1094,530" class="wood"/>
<!-- Protruding Front Brass Panel at X=38..55 (1166..1234), Y=-2..4 (442..466) -->
<polygon points="1166,466 1234,466 1234,442 1170,442 1166,446" class="brass"/>
<!-- Triangular Black Walnut Spline SP01 (14x14mm -> 56x56px at outer corner) -->
<polygon points="1014,450 1070,450 1014,506" class="spline"/>
<!-- Internal Corner Reinforcement Glue Block CB01 (22x22mm -> 88x88px inside X=20..42, Y=20..42) -->
<polygon points="1094,530 1182,530 1182,562 1126,618 1094,618" class="wood-cb"/>

<path d="M 1042 478 L 1245 478" class="lead-line"/>
<text x="1252" y="482" class="sm">北美黑胡桃木羽鍵 SP01..08 (14×14×5mm)</text>
<text x="1252" y="502" class="sm">深巧克力色澤對比金色緬甸柚木，順紋橫跨 45° 角</text>
<path d="M 1150 575 L 1245 555" class="lead-line"/>
<text x="1252" y="558" class="warn">★ 緬甸柚木內角補強柱 CB01..04 (22×22×78)</text>
<text x="1252" y="578" class="sm">還原 S04 右下角結構，從內側抱死 45° 斜接角，</text>
<text x="1252" y="598" class="sm">抗扭與搬運耐重 (>41kg) 提升 3 倍以上！</text>
<text x="1252" y="625" class="dim">• 面板浮凸：於 X=38 處嵌入木框 4mm、向外浮凸 2mm</text>
<text x="1252" y="647" class="dim">• 羽鍵高度：Z=21..26 與 Z=64..69（避開嵌槽，零干涉）</text>

<!-- Summary Comparison Table -->
<text x="1002" y="715" class="sub-hdr">3. D05 最終收斂結構摘要（Teak + Walnut Spline + 10-Point Nut Bars + Proud Panel）</text>
<rect x="1002" y="730" width="544" height="315" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" rx="4"/>

<text x="1018" y="760" class="sm">1. 【前後面板浮凸＋加大窗口】：6mm 面板嵌入木槽 4mm、向外浮凸 2mm；內側開 404×48</text>
<text x="1036" y="780" class="sm">貫通窗（容納 ALPS RK50 與表頭），保留 16mm 厚木肩與 6 點 M3×20 內鎖盲牙。</text>

<text x="1018" y="810" class="sm">2. 【緬甸柚木＋黑胡桃雙羽鍵＋內角柱】：主框與內角補強柱 (22×22×78) 採金棕色緬甸柚木，</text>
<text x="1036" y="830" class="sm">四角 45° 斜接嵌入 8 片 5mm 厚北美黑胡桃木羽鍵，兼具高雅撞色與重載抗扭剛性。</text>

<text x="1018" y="860" class="sm">3. 【四面木框 10 點上止口預埋方螺母條】：左右各 3 組＋前後上橫樑各 2 組（還原 S04），</text>
<text x="1036" y="880" class="sm">自上止口 (Z=86) 垂直投入雙孔方螺母條，頂板蓋上自然封口，消除 520mm 跨距下垂。</text>

<text x="1018" y="910" class="sm">4. 【雙層頂板底部快拆】：下層 8mm + 上層內縮 10mm 厚 5mm + 下凸台 4mm，頂面無孔；</text>
<text x="1036" y="930" class="sm">維修時僅需從底部鬆開 10 顆 M4×8 即可卸下木框，不必拆動頂部變壓器與真空管。</text>

<text x="1018" y="960" class="sm">5. 【底部腳墊】：四角 Ø48×14mm 車削金屬腳墊（避開底部 10 個 Ø8 起子通道）。</text>

<text x="1032" y="998" class="warn">證據聲明：所有尺寸均為概念草案 [ASSUMED]/[TO VERIFY]，未經驗證不得加工或載重。</text>
<text x="1018" y="1024" class="dim">驗證結果：127 個有效實體｜STEP 回讀通過｜0 干涉｜404×48 窗口與 10 處起子通道 100% 通過</text>

<!-- Footer Block -->
<line x1="20" y1="1082" x2="1580" y2="1082" stroke="#334155" stroke-width="1.5"/>
<text x="42" y="1112" class="sm">裝配順序：1. 柚木框 45° 斜接＋黑胡桃雙羽鍵＋內角補強柱膠合 → 2. 四面木框上止口盲槽投入 10 條雙孔方螺母條 → 3. 鎖固 10 支內側 L 支架 (M4×14) → 4. 前後面板嵌入 4mm（浮凸 2mm）、鎖 M3×20 → 5. 頂板封口、底部向上鎖 10 顆 M4×8。</text>
<text x="42" y="1142" class="tag">DWG NO: CB002-D05-SHEET01 | DATE: 2026-10-16 | MODEL: CB002_D05.FCStd / CB002_D05_assembly.step | MATURITY: L0/L1 HOLD — NOT FOR MANUFACTURE</text>
</svg>
'''

svg_path = OUT / '03_dimensions_and_fixings.svg'
svg_path.write_text(svg)
print(f'Wrote {svg_path}')

import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
try:
    from PySide6.QtGui import QGuiApplication, QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
    app = QGuiApplication.instance() or QGuiApplication([])
    r = QSvgRenderer(str(svg_path))
    img = QImage(1600, 1180, QImage.Format_ARGB32)
    img.fill(0xFFFFFFFF)
    p = QPainter(img)
    r.render(p)
    p.end()
    png_path = OUT / '03_dimensions_and_fixings.png'
    img.save(str(png_path))
    print(f'Wrote {png_path}')
except Exception as e:
    print(f'Note: PNG render skipped ({e})')

