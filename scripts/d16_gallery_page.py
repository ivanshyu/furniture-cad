# -*- coding: utf-8 -*-
from pathlib import Path
import json,html,csv,math,subprocess,sys
R=Path(__file__).resolve().parents[1]/'03_Cabinets/CB001_Curiosity_Low_Maple_Walnut/models/D16';O=R/'gallery';O.mkdir(exist_ok=True)
d=json.loads((R/'geometry_mm.json').read_text());colors={'WALNUT':'#826041','MAPLE':'#dec79e','GLASS':'#bbd7df','METAL':'#a48b51'};cn={'WALNUT':'胡桃木','MAPLE':'楓木','GLASS':'長虹玻璃','METAL':'金屬'}
def group(n):
 if n.startswith(('DOOR0','HANDLE0')):return '左門與把手'
 if n.startswith(('DOOR1','HANDLE1')):return '右門與把手'
 if n.startswith('POST'):return '立柱與雙色腳'
 if n.startswith('TOP') or ('RAIL' in n and '1405' in n):return '頂部'
 if n.startswith('BACK'):return '背板'
 if n.startswith('SHELF'):return '層板'
 if n.startswith('SIDE') and 'stretcher' not in n:return '側玻璃與飾條'
 if 'stretcher' in n:return '腳間橫條'
 return '底框與底板'
def subgroup(n):
 if n.startswith('HANDLE'):return ('左把手 H01' if n.startswith('HANDLE0') else '右把手 H02')
 if n.startswith('DOOR'):
  return ('左門' if n.startswith('DOOR0') else '右門')+('胡桃木框' if 'walnut' in n else '楓木飾條' if 'maple' in n else '玻璃')
 if n.startswith('POST'):return '上立柱' if n.endswith('upper') else '雙色腳 '+n.split('_')[1]
 if n.startswith('SIDE') and 'stretcher' not in n:return ('左側' if n.startswith('SIDE0') else '右側')+('玻璃' if 'GLASS' in n else '飾條')
 return group(n)
def component(n):
 if n.startswith('HANDLE'):return ('左把手 H01 · ' if n.startswith('HANDLE0') else '右把手 H02 · ')+('橢圓頭' if n.endswith('oval') else '接頸（暫定）' if 'neck' in n else '底座（暫定）')
 return n
rows=[]
for i,p in enumerate(d['parts']):
 v=p['vertices_mm'];s=[max(q[k] for q in v)-min(q[k] for q in v) for k in range(3)]
 rows.append({'id':f'P{i+1:03}','name':p['name'],'component':component(p['name']),'group':group(p['name']),'subgroup':subgroup(p['name']),'material':cn[p['material']],'x_mm':round(s[0],3),'y_mm':round(s[1],3),'z_mm':round(s[2],3)})
with (O/'D16_parts_dimensions.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
# Deterministic vector rendering of every actual mesh, individually laid out and labelled.
def projection(v):return (.82*v[0]+.57*v[1],.30*v[0]-.43*v[1]-v[2])
def cell(p,row,x,y):
 vs=[projection(v) for v in p['vertices_mm']];lo=[min(v[k] for v in vs) for k in range(2)];hi=[max(v[k] for v in vs) for k in range(2)]
 scale=min(265/max(hi[0]-lo[0],1),160/max(hi[1]-lo[1],1));pts=[(x+25+(v[0]-lo[0])*scale,y+52+(v[1]-lo[1])*scale) for v in vs]
 faces=sorted(p['faces'],key=lambda f:sum(p['vertices_mm'][j][0]-p['vertices_mm'][j][1]+p['vertices_mm'][j][2] for j in f)/len(f))
 a=[f'<g><rect x="{x}" y="{y}" width="330" height="290" rx="5" fill="white" stroke="#ccc"/><text x="{x+14}" y="{y+25}" font-size="16">{row["id"]} · {row["material"]}</text>']
 for f in faces:
  poly=' '.join(f'{pts[j][0]:.2f},{pts[j][1]:.2f}' for j in f)
  a.append(f'<polygon points="{poly}" fill="{colors[p["material"]]}" stroke="#574c3d" stroke-width=".22"/>')
 a.append(f'<text x="{x+12}" y="{y+240}" font-size="11">{html.escape(row["component"])}</text><text x="{x+12}" y="{y+263}" font-size="13">X {row["x_mm"]} × Y {row["y_mm"]} × Z {row["z_mm"]} mm</text></g>')
 return ''.join(a)
atlas=[]
for start in range(0,len(rows),9):
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 990"><rect width="1050" height="990" fill="#f0ece4"/><g font-family="sans-serif" fill="#292824"><text x="20" y="30" font-size="20">D16｜部件拆解索引 '+str(start//9+1)+'</text><text x="20" y="56" font-size="13">實際模型網格投影 · 尺寸為組裝座標 X/Y/Z 外形包絡，非開料／榫槽尺寸</text>'
 for k in range(start,min(start+9,len(rows))):svg+=cell(d['parts'][k],rows[k],15+(k-start)%3*345,80+(k-start)//3*300)
 svg+='</g></svg>';name=f'parts_{start//9+1:02}.svg';(O/name).write_text(svg,encoding='utf8');atlas.append(name)
(O/'parts_atlas.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>D16 全部件尺寸圖</title><style>body{margin:20px;background:#ece8df;font:16px system-ui}img{display:block;width:100%;max-width:1100px;margin:20px auto}@media print{img{break-before:page}}</style><h1>D16 · 99 個模型部件</h1><p>每件標記材質與X/Y/Z尺寸。實木腳的色塊為視覺模型分件，不代表製造時應拼成這些小塊。玻璃4.6 mm為模型紋理峰值厚度，非已選定玻璃規格。全部圖由模型程式投影產生，未用AI。</p><a href="D16_parts_dimensions.csv">下載完整尺寸CSV</a>'+''.join(f'<img src="{n}">' for n in atlas)+'</html>',encoding='utf8')
subprocess.run([sys.executable,str(Path(__file__).with_name('curiosity_d16_export.py'))],check=True)
p=R/'CB001_D16_viewer.html';s=p.read_text(encoding='utf8')
s=s.replace('</style>','''#layout{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,1fr);gap:14px;padding:14px}aside{background:#faf8f3;padding:16px;max-height:78vh;overflow:auto}aside img{width:100%;display:block}aside h2{font-size:18px;margin:0 0 10px}.thumbs{display:flex;flex-wrap:wrap;gap:5px}.thumbs button{font-size:13px;padding:5px}#viewport{height:75vh}#partinfo{font-size:14px;line-height:1.6}#partlist{width:100%;padding:8px}small{display:block;color:#665d50;margin:8px 0}@media(max-width:850px){#layout{grid-template-columns:1fr}aside{max-height:none}#viewport{height:65vh}}</style>''')
s=s.replace('<div id="viewport">','<div id="layout"><div id="viewport">')
s=s.replace('</div><footer>','''</div><aside><h2 id="imageTitle">透視 · AI材質效果</h2><div class="thumbs" id="galleryButtons"></div><p><a id="imageLink" target="_blank">放大圖片</a></p><img id="referenceImage" alt="固定視角參考圖"><small>AI材質效果僅供參考，局部比例與細節可能偏移；尺寸以左側D16模型及CAD底圖為準。旋轉模型時，圖片仍是最後選定的固定視角。</small><hr><h2>模型爆炸圖</h2><label><input id="exploded" type="checkbox">展開部件</label><p><input id="explodeAmount" type="range" min="0" max="1" step=".01" value="1" aria-label="爆炸距離"></p><select id="partlist" aria-label="選取部件"></select><p id="partinfo">選取零件查看材質與尺寸</p><a href="gallery/parts_atlas.html" target="_blank">全部99件：分解圖與尺寸</a> · <a href="gallery/D16_parts_dimensions.csv">CSV</a><small>爆炸圖直接使用模型網格，未使用AI。X/Y/Z為組裝座標的外形尺寸；視覺分件不是開料清單。</small></aside></div><footer>''')
s=s.replace('function view(pos,target){','function view(pos,target){controls.enableDamping=false;controls.update();')
s=s.replace('controls.update();}\nconst centre','controls.update();controls.enableDamping=true;}\nconst centre')
extra='''
const partRows=__ROWS__;
const viewNames={persp:'透視',front:'正面',side:'側面',top:'俯視',detail:'腳位近看',handles:'把手近看',bottom:'底板檢查'};
let selectedView='persp',imageKind='ai';
function updateImage(){const src='gallery/'+selectedView+'_'+imageKind+'.png';document.getElementById('referenceImage').src=src;document.getElementById('imageLink').href=src;document.getElementById('imageTitle').textContent=viewNames[selectedView]+' · '+(imageKind==='ai'?'AI材質效果':'原始3D底圖');}
for(const [id,name] of Object.entries(viewNames)){document.getElementById(id).addEventListener('click',()=>{selectedView=id;updateImage();});const b=document.createElement('button');b.textContent=name;b.onclick=()=>document.getElementById(id).click();document.getElementById('galleryButtons').appendChild(b);}
updateImage();
const sel=document.getElementById('partlist');sel.add(new Option('全部部件','-1'));partRows.forEach((p,i)=>sel.add(new Option(p.id+' · '+p.material+' · '+p.component,i)));
objects.forEach((o,i)=>{o.material=o.material.clone();o.userData.originalColor=o.material.color.clone();o.userData.row=partRows[i];});
function choose(i){sel.value=String(i);objects.forEach((o,k)=>{o.material.emissive.setHex(k===i?0x635017:0);});const p=partRows[i];document.getElementById('partinfo').textContent=p?p.id+'｜'+p.component+'｜'+p.material+'｜X '+p.x_mm+' × Y '+p.y_mm+' × Z '+p.z_mm+' mm':'全部部件';}
sel.onchange=()=>choose(Number(sel.value));
const ray=new THREE.Raycaster(),mouse=new THREE.Vector2();renderer.domElement.addEventListener('dblclick',e=>{const r=renderer.domElement.getBoundingClientRect();mouse.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);ray.setFromCamera(mouse,camera);const hit=ray.intersectObjects(objects.filter(o=>o.visible))[0];if(hit)choose(objects.indexOf(hit.object));});
function explode(){const a=document.getElementById('exploded').checked?Number(document.getElementById('explodeAmount').value):0;objects.forEach((o,i)=>{const p=partRows[i],n=p.name;let v=[0,0,0];if(n.startsWith('DOOR0')||n.startsWith('HANDLE0'))v=[-.28,-.55,0];else if(n.startsWith('DOOR1')||n.startsWith('HANDLE1'))v=[.28,-.55,0];else if(n.startsWith('TOP')||n.includes('1405'))v=[0,0,.4];else if(n.startsWith('BACK'))v=[0,.45,0];else if(n.startsWith('SHELF'))v=[0,-.2,.10];else if(n.startsWith('SIDE')&&!n.includes('stretcher'))v=[n.startsWith('SIDE0')?-.38:.38,0,0];else if(n.startsWith('POST'))v=[n.startsWith('POST_0')?-.13:.13,n.startsWith('POST_00')||n.startsWith('POST_10')?-.12:.12,0];else if(n.includes('stretcher'))v=[0,0,-.12];else v=[0,0,-.05];o.position.set(...v.map(x=>x*a));});}
document.getElementById('exploded').onchange=()=>{explode();if(document.getElementById('exploded').checked)view([-2.7,-4.5,2.6],[.34,.1,.85]);else document.getElementById('persp').click();};document.getElementById('explodeAmount').oninput=explode;
document.getElementById('wire').onchange=e=>objects.forEach(o=>o.material.wireframe=e.target.checked);
'''.replace('__ROWS__',json.dumps(rows,ensure_ascii=False))
s=s.replace('</script></body>',extra+'</script></body>');p.write_text(s,encoding='utf8')
subprocess.run([sys.executable,str(Path(__file__).with_name('d16_group_viewer.py'))],check=True)
subprocess.run([sys.executable,str(Path(__file__).with_name('d16_verify_inventory.py'))],check=True)
print('Gallery viewer + 11 exact mesh parts sheets + CSV ready')
