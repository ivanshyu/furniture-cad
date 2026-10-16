from pathlib import Path
p=Path(__file__).resolve().parents[1]/'output'/'D04'
s='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="980" viewBox="0 0 1200 980">
<style>text{font-family:Arial,'PingFang TC',sans-serif;fill:#263445;font-size:17px}.h{font-size:23px;font-weight:600}.sm{font-size:14px}.w{fill:#b78a63;stroke:#68462f;stroke-width:1.5}.a{fill:#e5cb8b;stroke:#8b702d;stroke-width:1.5}.s{fill:#b3c3d0;stroke:#465c70;stroke-width:1.5}.d{fill:none;stroke:#587082;stroke-width:1.3}.ghost{fill:none;stroke:#587082;stroke-dasharray:5 4}</style>
<rect width="1200" height="980" fill="#f7f8fa"/>
<text x="40" y="45" class="h">CB002 / D04 — 頂面無螺絲 · 底部拆裝</text>
<text x="40" y="76">概念剖面，不按比例製造。所有尺寸 mm；2026-10-12 · 非原廠結構確認。</text>
<text x="40" y="123" class="h">A. 頂板台階與隱藏固定（左側剖面）</text>
<!-- wood 20mm thick; top z=90 at svg y=230 -->
<rect x="120" y="230" width="120" height="290" class="w"/>
<!-- outer top shoulder 4mm thick; lower locating step 4mm -->
<path d="M120 206 H550 V254 H243 V230 H120 Z" class="a"/>
<!-- L bracket 3mm thick -->
<path d="M240 254 H408 V272 H258 V386 H240 Z" class="s"/>
<!-- underside blind pilot 6mm upward from underside -->
<rect x="332" y="218" width="20" height="36" class="ghost"/>
<!-- washer1, vertical M4x8 shaft, head -->
<rect x="315" y="272" width="54" height="6" class="s"/>
<rect x="330" y="230" width="24" height="48" class="s"/>
<rect x="321" y="278" width="42" height="18" class="s"/>
<!-- side wall insert x10..20, M4x12 pointing left -->
<rect x="180" y="320" width="60" height="36" class="a"/>
<rect x="258" y="311" width="6" height="54" class="s"/>
<rect x="192" y="326" width="72" height="24" class="s"/>
<rect x="264" y="317" width="18" height="42" class="s"/>
<!-- tool access -->
<path d="M342 490 V308 M334 320 L342 308 L350 320" class="d"/>
<text x="290" y="516">工具由底部進入 ↑</text>
<text x="124" y="552">木側板20厚</text>
<text x="82" y="184">機外</text><text x="483" y="184">機內</text>
<path d="M550 217 H580" class="d"/><text x="595" y="220">頂面完整無孔</text>
<path d="M490 244 H580" class="d"/><text x="595" y="250">周邊4厚／中心8厚；下緣台階伸入4</text>
<path d="M408 262 H580" class="d"/><text x="595" y="282">L支架厚3，承接頂板下緣</text>
<path d="M369 285 L550 312 H580" class="d"/><text x="595" y="316">M4×8由下向上鎖入底面盲牙</text>
<text x="595" y="344">墊片1＋支架3＋入牙4＝8</text>
<path d="M282 344 L550 375 H580" class="d"/><text x="595" y="381">側向M4×12鎖入木用嵌件</text>
<text x="595" y="409">每支架2枚；共6支架、12個嵌件</text>
<text x="595" y="450">定位凸台與木內口：每側暫留0.5</text>
<text x="595" y="478">長孔留在支架，不穿透頂板</text>
<text x="595" y="514" class="sm">嵌件、孔底餘厚、木材活動與夾緊力待試件驗證。</text>
<path d="M40 585 H1160" class="d"/>
<text x="40" y="627" class="h">B. 前後面板：只留外側嵌槽，不再挖中央窗口</text>
<rect x="120" y="660" width="120" height="150" class="w"/>
<rect x="120" y="675" width="36" height="120" class="a"/>
<rect x="133" y="720" width="108" height="12" class="s"/>
<rect x="240" y="705" width="6" height="42" class="s"/>
<rect x="246" y="709" width="12" height="34" class="s"/>
<text x="315" y="686">外側鋁板6厚，放入深6嵌槽。</text>
<text x="315" y="718">剩餘木料14完整保留，僅鑽局部螺絲過孔。</text>
<text x="315" y="750">M3×18：墊片1＋木料14＋鋁板入牙3。</text>
<text x="315" y="782">無中央窗口、無螺絲頭沉孔；螺絲頭在機內。</text>
<path d="M40 848 H1160" class="d"/>
<text x="40" y="887">装配：側壁嵌件 → L支架 → 前後板 → 頂板由上放入 → 從底部向上鎖緊。</text>
<text x="40" y="918">底板與腳座未設計；未驗算承重／散熱／電氣安全。不得直接加工、載重或通電。</text>
<text x="40" y="953" class="sm">CB002-D04-01 / Concept / Material grades &amp; tolerances TBD / Maturity L0–L1 HOLD</text>
</svg>'''
(p/'03_dimensions_and_fixings.svg').write_text(s)
