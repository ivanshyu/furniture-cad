"""Build current Ø520 / full-thickness double-band Pages assets. No deployment."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1]
B=R/'02_Tables/TB001_D16_Three_Tier/models/D07'
S=B/'variants/upper_double_lines';D=R/'docs/tb001'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(source):
 g=source/'gallery';m=json.loads((g/'ai_manifest_all_v1.json').read_text())
 assert m['geometry_sha256']==digest(source/'geometry_mm.json'),'AI reference geometry stale'
 assert m['prompts_sha256']==digest(g/'ai_prompts_all_v1.json')
 views=json.loads((source/'views.json').read_text());prompts=json.loads((g/'ai_prompts_all_v1.json').read_text())
 assert set(views)==set(m['views'])==set(prompts)
 for k,e in m['views'].items():
  assert e['camera']==views[k],k
  assert e['input_sha256']==digest(g/e['input']),k
  assert e['output_sha256']==digest(g/e['output']),k
  assert e['prompt_sha256']==hashlib.sha256(prompts[k].encode()).hexdigest(),k
 return m
m=validate(S);assert len(m['views'])==7
archive=R/'docs/tb001-d06'
assert archive.exists(),'Preserve old square-table page before replacing it'
D.mkdir(exist_ok=True)
files=['TB001_D07.FCStd','TB001_D07.step','TB001_D07.glb','dimensions.svg','preview.png','parts.csv','README.md','parameters.json','model_checks.json','views.json']
for f in files:shutil.copy2(S/f,D/f)
shutil.copytree(S/'gallery',D/'gallery',dirs_exist_ok=True)
s=(S/'TB001_D07_viewer.html').read_text().replace('Round Arch · 上方雙橫線試款','Round Arch · 雙橫段圓桌')
s=s.replace('<a href="../../TB001_D07_viewer.html">← 回到無橫線基準版</a>','<a href="../index.html">← 專案總覽</a> · <a href="../tb001-d06/">D06 方形茶几歷史版</a>')
(D/'index.html').write_text(s);(D/'TB001_D07_viewer.html').write_text(s)
# Retain the previously shared variant URL, now identical geometry/gallery.
V=D/'variants/upper_double_lines';V.mkdir(parents=True,exist_ok=True)
for f in files:shutil.copy2(S/f,V/f)
shutil.copytree(S/'gallery',V/'gallery',dirs_exist_ok=True)
vs=(S/'TB001_D07_viewer.html').read_text().replace('← 回到無橫線基準版','← 回到茶几主頁')
(V/'TB001_D07_viewer.html').write_text(vs)
f=R/'docs/index.html';s=f.read_text();a=s.index('<a class="card" href="tb001/"');b=s.index('</a>',a)+4
s=s[:a]+'''<a class="card" href="tb001/"><div class="image"><img src="tb001/gallery/perspective_ai_square_v1.png?v=lower520-double-bands" alt="Ø520下層與雙胡桃橫段楓木圓桌"></div><div class="body"><div class="meta"><span>TB001 / SIDE TABLE</span><span>D07 · L1</span></div><h3>Round Arch / Double Bands</h3><p>上板 Ø650、下板 Ø520、總高550 mm。楓木拱頂腳、全厚雙胡桃橫段與三層 X；七視角 AI／CAD 圖庫及原生實體下載。</p><div class="go"><b>開啟圓桌專案</b><span>View model →</span></div></div></a>'''+s[b:];f.write_text(s)
print('Current Ø520 seven-view main page built; square D06 retained in archive.')
