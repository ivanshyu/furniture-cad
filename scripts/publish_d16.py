"""Build GitHub Pages docs from the D16 source. Run from any directory."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
src=root/'03_Cabinets/CB001_Curiosity_Low_Maple_Walnut/models/D16'
out=root/'docs';out.mkdir(exist_ok=True);(out/'gallery').mkdir(exist_ok=True)
shutil.copy2(src/'CB001_D16_viewer.html',out/'CB001_D16_viewer.html')
(out/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=CB001_D16_viewer.html"><a href="CB001_D16_viewer.html">D16 Viewer</a>',encoding='utf8')
(out/'.nojekyll').touch()
files=list((src/'gallery').glob('*_ai.png'))+list((src/'gallery').glob('parts_*.svg'))+[src/'gallery'/n for n in ['parts_atlas.html','D16_parts_dimensions.csv','verification.html']]
for p in files:shutil.copy2(p,out/'gallery'/p.name)
print('Built docs:',len(files)+3,'files')
