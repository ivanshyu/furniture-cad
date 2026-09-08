# -*- coding: utf-8 -*-
"""Export Blender source mesh to CAD DXF and standalone interactive viewer."""
import json
from pathlib import Path
import ezdxf
ROOT=Path(__file__).resolve().parents[1]/'03_Cabinets/CB001_Curiosity_Low_Maple_Walnut'
OUT=ROOT/'models/D16';data=json.loads((OUT/'geometry_mm.json').read_text())
d=ezdxf.new('R2010');d.units=4
colors={'METAL':(137,108,62),'WALNUT':(110,72,47),'MAPLE':(211,179,119),'GLASS':(139,195,204)}
for n,c in colors.items():d.layers.new(n,dxfattribs={'true_color':ezdxf.colors.rgb2int(c)})
m=d.modelspace()
for part in data['parts']:
    mesh=m.add_mesh(dxfattribs={'layer':part['material']})
    with mesh.edit_data() as edit:edit.vertices=part['vertices_mm'];edit.faces=part['faces']
d.saveas(OUT/'CB001_D16_3D_mesh.dxf')
check=ezdxf.readfile(OUT/'CB001_D16_3D_mesh.dxf');assert not check.audit().has_errors
html='''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Curiosity Cabinet D16 — CAD 3D</title>
<style>body{margin:0;background:#eeeae3;color:#292824;font:16px system-ui}header{padding:20px 28px;background:#faf8f3}h1{font-size:21px;margin:0 0 6px}p{margin:6px 0;color:#625e57}nav{display:flex;gap:10px;flex-wrap:wrap;padding:12px 28px;background:#faf8f3}button,label{padding:8px 12px;border:1px solid #c7bfae;border-radius:5px;background:white;color:#292824}#viewport{height:75vh;min-height:450px;position:relative}canvas{display:block}#status{position:absolute;left:24px;top:14px;color:#625e57;font-size:14px}footer{padding:12px 28px;font-size:14px}</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script></head><body>
<header><h1>Curiosity Cabinet · CAD 幾何 D16</h1><p>685 × 404.66 × 1430 mm（含門）｜前凸 34.66 mm｜楓木飾條 9 mm｜胡桃木門框 22 mm｜櫃身柱30×40 mm／內收腳40 mm</p></header>
<nav><button id="persp">透視</button><button id="front">正面</button><button id="side">側面</button><button id="top">俯視</button><button id="detail">腳位近看</button><button id="handles">把手近看</button><button id="bottom">底板檢查</button><label><input id="glass" type="checkbox" checked>顯示玻璃</label><label><input id="wire" type="checkbox">線框</label><label><input id="back" type="checkbox" checked>暫定背板</label></nav>
<div id="viewport"><span id="status">正在載入 3D 顯示元件…</span></div><footer>拖曳旋轉・滾輪縮放・右鍵平移。與渲染及3D DXF共用幾何；這裡的玻璃採簡化透明顯示。首次開啟需連線載入顯示元件。尺寸為方案參數，非製造發布。</footer>
<script type="module">
import * as THREE from 'three';import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const data=__DATA__,root=document.getElementById('viewport'),status=document.getElementById('status');
const scene=new THREE.Scene();scene.background=new THREE.Color('#eeeae3');
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));root.appendChild(renderer.domElement);
const camera=new THREE.PerspectiveCamera(35,1,.001,100);camera.up.set(0,0,1);const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
scene.add(new THREE.HemisphereLight(0xffffff,0x897d6a,2));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(-2,-3,4);scene.add(light);
const mats={METAL:new THREE.MeshStandardMaterial({color:'#896c3e',metalness:.75,roughness:.32}),WALNUT:new THREE.MeshStandardMaterial({color:'#705037',roughness:.5}),MAPLE:new THREE.MeshStandardMaterial({color:'#dbc391',roughness:.48}),GLASS:new THREE.MeshStandardMaterial({color:'#adcbd0',transparent:true,opacity:.12,roughness:.2,depthWrite:false,side:THREE.DoubleSide})};
const objects=[];for(const p of data.parts){const g=new THREE.BufferGeometry(),a=[];for(const f of p.faces){for(let i=1;i<f.length-1;i++){for(const j of [f[0],f[i],f[i+1]])a.push(...p.vertices_mm[j].map(x=>x/1000));}}g.setAttribute('position',new THREE.Float32BufferAttribute(a,3));g.computeVertexNormals();const o=new THREE.Mesh(g,mats[p.material]);o.name=p.name;o.userData.kind=p.material;scene.add(o);objects.push(o);}
const grid=new THREE.GridHelper(2,20,0xc3b8a5,0xdad3c8);grid.rotation.x=Math.PI/2;grid.position.set(.3425,.2,-.002);scene.add(grid);
function view(pos,target){grid.visible=pos[2]>=0;camera.position.set(...pos);controls.target.set(...target);controls.update();}
const centre=[.3425,.17,.715];document.getElementById('persp').onclick=()=>view([-2,-3,1.9],centre);document.getElementById('front').onclick=()=>view([.3425,-3.4,.715],centre);document.getElementById('side').onclick=()=>view([-3,.20233,.715],centre);document.getElementById('top').onclick=()=>view([.3425,.20233,3.4],centre);document.getElementById('detail').onclick=()=>view([-.35,-.75,.55],[.08,.055,.22]);
document.getElementById('handles').onclick=()=>view([.65,-.8,.97],[.3425,-.04,.865]);
document.getElementById('bottom').onclick=()=>view([1,-1,-.6],[.3425,.185,.305]);
document.getElementById('glass').onchange=e=>objects.filter(o=>o.userData.kind==='GLASS').forEach(o=>o.visible=e.target.checked);
document.getElementById('back').onchange=e=>objects.filter(o=>o.name.startsWith('BACK')).forEach(o=>o.visible=e.target.checked);
document.getElementById('wire').onchange=e=>{mats.WALNUT.wireframe=e.target.checked;mats.MAPLE.wireframe=e.target.checked;};
const resize=()=>{renderer.setSize(root.clientWidth,root.clientHeight);camera.aspect=root.clientWidth/root.clientHeight;camera.updateProjectionMatrix();};new ResizeObserver(resize).observe(root);resize();view([-2,-3,1.9],centre);status.textContent='同一套CAD幾何・可旋轉檢視';
renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera);});window.cabinetCheck={partCount:objects.length,bead:data.parameters.maple_bead};
</script></body></html>'''
(OUT/'CB001_D16_viewer.html').write_text(html.replace('__DATA__',json.dumps(data,separators=(',',':'))),encoding='utf-8')
(OUT/'model_checks.json').write_text(json.dumps({'mesh_count':len(data['parts']),'dxf_mesh_count':len(check.modelspace().query('MESH')),'audit_errors':len(check.audit().errors),'units':'mm','CAD_is_mesh_not_solid':True},indent=2))
print('3D CAD and viewer exported:',len(data['parts']),'parts')
