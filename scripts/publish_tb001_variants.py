"""Validate and mirror Blender/AI table variants into Pages, preserving baselines."""
from pathlib import Path
import hashlib,json,shutil,re
R=Path(__file__).resolve().parents[1]
B=R/'02_Tables/TB001_D16_Three_Tier/models/D07/variants'
variants=[('snug_slot_20','四腳 · 滿槽三層 X'),('three_leg_triangle','三腳 · 三條三角框'),('three_leg_triangle_two','三腳 · 兩條三角框')]
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for v,title in variants:
 s=B/v;g=s/'gallery';bm=json.loads((g/'blender_manifest.json').read_text());am=json.loads((g/'ai_blender_manifest_v1.json').read_text())
 assert bm['geometry_sha256']==am['geometry_sha256']==h(s/'geometry_mm.json')
 assert bm['views_sha256']==am['views_sha256']==h(s/'views.json')
 assert am['prompts_sha256']==h(g/'ai_prompts_blender_v1.json')
 assert set(bm['views'])==set(am['views'])==set(json.loads((s/'views.json').read_text()))
 for key,a in am['views'].items():
  b=bm['views'][key]
  assert a['input']==b['output'] and a['input_sha256']==b['sha256']==h(g/a['input'])
  assert a['sha256']==h(g/a['output'])
 checks=json.loads((s/'model_checks.json').read_text())
 assert checks['all_solids_valid'] and not checks['positive_volume_collisions']
 shutil.copytree(s,R/'docs/tb001/variants'/v,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.FCBak','*.blend1','*.FCStd1','history'))
cards=[]
for v,title in variants:
 url='tb001/variants/'+v
 cards.append(f'<a class="card" href="{url}/TB001_D07_viewer.html"><div class="image"><img loading="lazy" src="{url}/gallery/perspective_ai_v1.png" alt="{title}"></div><div class="body"><div class="meta"><span>TB001 / VARIANT</span><span>D07 · L1</span></div><h3>{title}</h3><p>上板 Ø650、下板 Ø520、總高 550 mm。互動 CAD、七視角 AI／Blender 切換。承重接合與抗傾覆未驗證。</p><div class="go"><b>開啟此版本</b><span>View model →</span></div></div></a>')
p=R/'docs/index.html';s=p.read_text();s=re.sub(r'<!-- TB001_VARIANTS_START -->.*?<!-- TB001_VARIANTS_END -->','',s,flags=re.S)
s=s.replace('</section></main>','<!-- TB001_VARIANTS_START -->'+''.join(cards)+'<!-- TB001_VARIANTS_END --></section></main>');p.write_text(s)
nav='<nav style="padding:20px 36px;line-height:2"><a href="../index.html">← 專案總覽</a> · '+ ' · '.join(f'<a href="variants/{v}/TB001_D07_viewer.html">{title}</a>' for v,title in variants)+'</nav>'
for name in ['index.html','TB001_D07_viewer.html']:
 p=R/'docs/tb001'/name;s=p.read_text();s=re.sub(r'<!-- VARIANT_NAV_START -->.*?<!-- VARIANT_NAV_END -->','',s,flags=re.S);s=s.replace('<body>','<body><!-- VARIANT_NAV_START -->'+nav+'<!-- VARIANT_NAV_END -->');p.write_text(s)
print('Validated and published three variant directories; overview and baseline navigation updated.')
