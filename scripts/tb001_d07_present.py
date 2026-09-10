#!/usr/bin/env python3
"""Presentation derived only from D07 CAD meshes; no AI render substitution."""
import json
from pathlib import Path
import os
import tb001_gallery_render as raster
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('TB001_D07_OUT',str(ROOT/'02_Tables/TB001_D16_Three_Tier/models/D07')))
data=json.loads((OUT/'geometry_mm.json').read_text());p=json.loads((OUT/'parameters.json').read_text())
views={
 'perspective':dict(position=[.95,-1.6,1.02],target=[0,0,.3],up=[0,0,1],span=.83),
 'front':dict(position=[0,-2,.3],target=[0,0,.3],up=[0,0,1],span=.78),
 'top':dict(position=[0,0,3],target=[0,0,.3],up=[0,1,0],span=.78),
 'structure':dict(position=[.95,-1.6,.85],target=[0,0,.3],up=[0,0,1],span=.8),
 'grip':dict(position=[.12,-.22,1.05],target=[0,0,.59],up=[0,0,1],span=.22),
 'x_detail':dict(position=[.6,-.95,1.0],target=[0,0,.27],up=[0,0,1],span=.57)}
# Camera targets follow the changed overall height and component elevations.
centre=p['overall_height']/2000
for name,spec in views.items():
 if name in ['perspective','front','top','structure']:
  spec['target']=[0,0,centre]
  if name=='front':spec['position'][2]=centre
  spec['span']=max(p['top_diameter'],p['overall_height'])/1000*1.3
# Low perspective view through the gap between the two front legs.
for name in ['perspective','structure']:
 views[name]['position']=[0,-4,centre+1.025]
 views[name]['projection']='perspective'
views['grip']['target']=[0,0,(p['overall_height']-p['top_thickness']/2)/1000]
views['grip']['position']=[.12,-.22,p['overall_height']/1000+.45]
views['x_detail']['target']=[0,0,(p['shelf_top']-p['shelf_thickness']-2.5*p['x_height'])/1000]
views['x_detail']['span']=2*(p['leg_radius']+p['leg_thickness']/2+p['x_projection'])/1000*1.3
if p.get('gallery_set')=='cabinet_seven':
 views.pop('x_detail')
 views['side']=dict(position=[-2,0,centre],target=[0,0,centre],up=[0,0,1],span=.845)
 views['bottom']=dict(position=[.9,-1.5,-1.2],target=[0,0,centre],up=[0,0,1],span=.845)
(OUT/'views.json').write_text(json.dumps(views,indent=2)+'\n')
gallery=OUT/'gallery';gallery.mkdir(exist_ok=True)
raster.DATA=data;raster.COLORS={'MAPLE':'e5d6b5','WALNUT':'63432e'}
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',17)
sheet=Image.new('RGB',(1800,140+660*((len(views)+2)//3)),'#f4f0e8');d=ImageDraw.Draw(sheet)
d.text((35,24),'TB001 / D07 — ROUND ARCH / COMPACT X',font=font,fill='#382e25')
d.text((35,62),'Actual BRep CAD / solid maple + walnut / all sizes provisional / L1 — NOT FOR PRODUCTION',font=small,fill='#776754')
for i,(name,spec) in enumerate(views.items()):
 raster.DATA={'parts':[x for x in data['parts'] if (x['group']=='x_rail' if name=='x_detail' else name!='structure' or x['group'] not in ['upper_top','lower_top','grip_trim'])]}
 im=raster.render(spec);im.save(gallery/f'{name}_cad.png')
 x=25+i%3*595;y=105+i//3*660
 sheet.paste(im.resize((555,616),Image.Resampling.LANCZOS),(x,y));d.text((x,y+620),name.upper()+' / CAD',font=small,fill='#382e25')
sheet.save(OUT/'preview.png')
# Reuse the shared viewer's triangle rendering, with D07-specific content/cameras.
src=(ROOT/'scripts/tb001_viewer.html').read_text()
start=src.index('<script type="module">');script=src[start:]
script=script.replace('const data=__DATA__','const data='+json.dumps(data,separators=(',',':')))
script=script.replace('MAPLE:0xd9bd89','MAPLE:0xe5d6b5')
script=script.replace('const camera=new THREE.OrthographicCamera','let camera=new THREE.OrthographicCamera')
script=script.replace('renderer.setSize(w,h);','if(camera.isPerspectiveCamera){camera.aspect=a;camera.fov=2*Math.atan(span/(2*camera.position.distanceTo(controls.target)))*180/Math.PI;camera.updateProjectionMatrix();}renderer.setSize(w,h);')
script=script.replace('const controls=new OrbitControls','let controls=new OrbitControls')
a=script.index("let viewName='persp';");b=script.index('function resize()',a)
script=script[:a]+'''function view(name){
 const views={persp:[.95,-1.6,1.02],front:[0,-2,.3],side:[-2,0,.3],top:[0,0,3],bottom:[0,0,-3]};
 controls.dispose();camera=name==='persp'?new THREE.PerspectiveCamera(12,host.clientWidth/host.clientHeight,.01,20):new THREE.OrthographicCamera(-.6,.6,.6,-.6,.001,20);camera.up.set(...(['top','bottom'].includes(name)?[0,1,0]:[0,0,1]));
 camera.position.set(...views[name]);controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
 controls.target.set(0,0,.3+Number(document.querySelector('#explode').value)*.14);camera.zoom=1;camera.updateProjectionMatrix();controls.update();resize();
}
''' +script[b:]
script=script.replace("{Legs:0,'Side lines':0,Structure:0,Lower:.10,Middle:.25,Top:.42}","{upper_top:.42,grip_trim:.42,lower_top:.12}")
script=script.replace('ray.intersectObjects(objects)[0]','ray.intersectObjects(objects.filter(o=>o.visible))[0]')
script=script.replace("p.size_mm.join(' × ')","p.size_mm.map(v=>v.toFixed(1)).join(' × ')")
script=script.replace("document.querySelector('#status').textContent='同一套尺寸幾何 · '+objects.length+' 個視覺分件';window.tb001Check={partCount:objects.length,ready:true,boundsMM:[data.parameters.overall_width??data.parameters.width,data.parameters.depth,data.parameters.height]};", "document.querySelector('#status').textContent='FreeCAD 實體衍生 · '+objects.length+' 個零件';window.tb001Check={partCount:objects.length,ready:true,boundsMM:[600,600,600]};document.querySelector('#structure').onchange=e=>{objects.forEach((o,i)=>o.visible=!(e.target.checked&&['upper_top','lower_top','grip_trim'].includes(data.parts[i].group)));};")
script=script.replace('persp:[.95,-1.6,1.02]', 'persp:'+json.dumps(views['perspective']['position']))
script=script.replace('boundsMM:[600,600,600]', 'boundsMM:'+json.dumps([p['top_diameter'],p['top_diameter'],p['overall_height']]))
script=script.replace('target.set(0,0,.3+',f'target.set(0,0,{centre}+').replace('controls.target.z=.3+',f'controls.target.z={centre}+')
script=script.replace('(.87+',f'({max(p["top_diameter"],p["overall_height"])/1000*1.3}+')
head=src[:src.index('</head>')]
head=head.replace('TB001 · D16 三層邊几','TB001 D07 · Round Arch')
body='''</head><body><header><small>TB001 / D07 · CAD DRAFT</small><h1>Round Arch · 緊密三層 X</h1><p>全楓木雙圓板／四隻拱頂板腳／胡桃木框縫。僅上桌面開小型矩形孔。</p></header>
<main><div id="view"><img id="fallback" src="gallery/perspective_cad.png" alt="D07 CAD"><span id="status">載入互動模型…</span></div>
<aside><small>暫定尺寸 · mm</small><div class="metric">Ø600 × H600</div><p>下圓板 Ø420／面高 320<br>上孔淨空 95 × 30／R3<br>胡桃框寬 4／外廓 103 × 38<br>X 桿高 14／淨間隔 14</p>
<nav><button data-view="persp">立體</button><button data-view="front">正面</button><button data-view="side">側面</button><button data-view="top">俯視</button><button data-view="bottom">底視</button></nav>
<label><input id="structure" type="checkbox"> 隱藏桌板，檢查承托</label>
<label>桌板分離檢視 <input id="explode" type="range" min="0" max="1" step=".01" value="0"></label>
<label>零件 <select id="parts"><option value="">全部部件</option></select></label><div id="partInfo">拖曳旋轉、滾輪縮放；點選零件。分離檢視不是裝配順序。</div>
<p id="loadError">互動元件未載入，可查看 CAD 靜態圖或下載原生模型。</p>
<div class="rule"><a href="TB001_D07.FCStd">FreeCAD 原生實體</a><br><a href="TB001_D07.step">STEP 實體交換檔</a><br><a href="TB001_D07.glb">GLB 預覽</a><br><a href="dimensions.svg">尺寸草圖</a><br><a href="parts.csv">零件表（非開料表）</a><br><a href="README.md">工程待辦／重建方式</a></div></aside></main>
<details open><summary>同一實體 CAD 六視圖</summary><img src="preview.png" alt="CAD views"></details>
<footer>L1 工程草稿，非施工圖。尺寸待確認；桌板固定、腳墊接合、伸縮與承重未完成驗證；開孔尚不可視為承重提把。互動視窗使用網路載入 Three.js，靜態圖可離線查看。</footer>
'''
body=body.replace('Ø600 × H600',f'Ø{p["top_diameter"]} × H{p["overall_height"]}').replace('Ø420／面高 320',f'Ø{p["shelf_diameter"]}／面高 {p["shelf_top"]}').replace('95 × 30／R3',f'{p["grip_clear_length"]} × {p["grip_clear_width"]}／R{p["grip_corner_radius"]}').replace('框寬 4／外廓 103 × 38',f'框寬 {p["grip_trim"]}／外廓 {p["grip_clear_length"]+2*p["grip_trim"]} × {p["grip_clear_width"]+2*p["grip_trim"]}').replace('桿高 14／淨間隔 14',f'桿高 {p["x_height"]}／淨間隔 {p["x_height"]}')
if (OUT/'gallery/perspective_ai_square_v1.png').exists():
 body=body.replace('<details open><summary>同一實體 CAD 六視圖', (ROOT/'scripts/tb001_d07_gallery.html').read_text().replace("{perspective:'透視',front:'正面',top:'俯視',structure:'承托結構',grip:'開孔細節',x_detail:'X 接合'}",json.dumps({k:{'perspective':'透視','front':'正面','top':'俯視','structure':'承托結構','grip':'開孔細節','x_detail':'X 接合','side':'側面','bottom':'底部'}[k] for k in views},ensure_ascii=False)).replace('六個視角',str(len(views))+' 個視角')+'<details><summary>同一實體 CAD 六視圖')
listener="""document.addEventListener('d07-gallery-view',e=>{
 const spec=__VIEWS__[e.detail];if(!spec)return;
 controls.dispose();camera=spec.projection==='perspective'?new THREE.PerspectiveCamera(12,1,.01,20):new THREE.OrthographicCamera(-.6,.6,.6,-.6,.001,20);
 camera.up.set(...spec.up);camera.position.set(...spec.position);controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.target.set(...spec.target);
 document.querySelector('#explode').value=0;
 objects.forEach((o,i)=>{o.position.copy(o.userData.original);const role=data.parts[i].group;o.visible=e.detail==='x_detail'?role==='x_rail':e.detail!=='structure'||!['upper_top','lower_top','grip_trim'].includes(role);});
 document.querySelector('#structure').checked=['structure','x_detail'].includes(e.detail);
 resize();const aspect=host.clientWidth/host.clientHeight,span=spec.span*Math.max(1,1/aspect);
 if(camera.isPerspectiveCamera)camera.fov=2*Math.atan(span/(2*camera.position.distanceTo(controls.target)))*180/Math.PI;
 else{camera.left=-span*aspect/2;camera.right=span*aspect/2;camera.top=span/2;camera.bottom=-span/2;}
 camera.updateProjectionMatrix();controls.update();
});
""".replace('__VIEWS__',json.dumps(views))
script=script.replace("document.querySelector('#status').textContent='FreeCAD",listener+"document.querySelector('#status').textContent='FreeCAD")
if p.get('variant')=='upper_double_lines':
 body=body.replace('<h1>Round Arch · 緊密三層 X</h1>','<h1>Round Arch · 上方雙橫線試款</h1>').replace('<p>全楓木雙圓板','<p>每腳兩段 14 mm 高胡桃木橫段；間隙 14 mm、貫穿 20 mm 腳厚、距拱起點 __BAND_CLEARANCE__ mm。楓木脚分為三段，承重接合尚未設計。僅 CAD 試款，尚無此款 AI 渲染。</p><p>全楓木雙圓板')
 body=body.replace('__BAND_CLEARANCE__',str(p['upper_band_crown_clearance']))
 body=body.replace('<main>','<p style="padding:0 36px"><a href="../../TB001_D07_viewer.html">← 回到無橫線基準版</a></p><main>')
elif (OUT/'variants/upper_double_lines/TB001_D07_viewer.html').exists():
 body=body.replace('<main>','<p style="padding:0 36px"><a href="variants/upper_double_lines/TB001_D07_viewer.html">查看上方雙胡桃橫線 CAD 試款 →</a>（基準版與 AI 圖維持不變）</p><main>')
body=body.replace('同一實體 CAD 六視圖',f'同一實體 CAD {len(views)} 視圖')
if p.get('gallery_set')=='cabinet_seven' and (OUT/'gallery/ai_manifest_all_v1.json').exists():
 body=body.replace('僅 CAD 試款，尚無此款 AI 渲染。','已提供此款七視角 AI／CAD 對照。')
(OUT/'TB001_D07_viewer.html').write_text(head+body+script)
print('CAD previews and D07 interactive viewer written')
