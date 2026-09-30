import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {Rhino3dmLoader} from 'three/addons/loaders/3DMLoader.js';
const $=id=>document.getElementById(id), root=$('viewport');
const scene=new THREE.Scene();scene.background=new THREE.Color('#eeeae3');
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));root.prepend(renderer.domElement);
const camera=new THREE.PerspectiveCamera(35,1,1,100000);camera.up.set(0,0,1);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
scene.add(new THREE.HemisphereLight(0xffffff,0x897d6a,2));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(-2000,-3000,4000);scene.add(light);
const grid=new THREE.GridHelper(2400,24,0xc3b8a5,0xdad3c8);grid.rotation.x=Math.PI/2;grid.position.z=-2;scene.add(grid);
const objects=[],rows=[],tags=[],snapshots={};let chosen=-1,overall,ready=false;
const groups={B01:'靠背區',S01:'座面區',F01:'左框區',F02:'右框區'};
const offsets={B01:[0,160,280],S01:[0,-250,80],F01:[-260,0,0],F02:[260,0,0]};
const colors={B01:0x8f5335,S01:0xcf9a64,F01:0x9f6844,F02:0xb37d52};
const viewNames={persp:'透視',front:'正面',side:'側面',top:'俯視',detail:'腳位近看',handles:'扶手近看',bottom:'座底檢查'};
// Geometric zones are inferred, not authoritative joinery boundaries.
function classify(c,s){
 if(c.z>600 || (c.z>550 && s.x>300))return ['B01',c.z>600?'靠背曲面':'後橫板曲面'];
 if(c.z<430 && s.x>300)return ['S01',s.y>100?'座面曲面':c.y<200?'前橫檔曲面':'後橫檔曲面'];
 const g=c.x<315?'F01':'F02';
 return [g,c.z>=550&&s.z<50?'扶手曲面':s.z>400&&s.y>100?'側支撐曲面':s.z>400||c.z<1&&s.y<50?(c.y<200?'前腳曲面':'後腳曲面'):c.z<120?'下橫檔曲面':'其餘曲面'];
}
function boxOf(list){const b=new THREE.Box3();list.forEach(o=>b.expandByObject(o));return b;}
function aim(b,dir=new THREE.Vector3(-1,-1.8,.9),cam=camera){
 const c=b.getCenter(new THREE.Vector3()),r=Math.max(1,b.getSize(new THREE.Vector3()).length()/2);
 const angle=Math.min(THREE.MathUtils.degToRad(cam.fov/2),Math.atan(Math.tan(THREE.MathUtils.degToRad(cam.fov/2))*cam.aspect));
 cam.position.copy(c).add(dir.clone().normalize().multiplyScalar(r/Math.sin(angle)*1.15));cam.lookAt(c);
 if(cam===camera){controls.enableDamping=false;controls.target.copy(c);controls.update();controls.enableDamping=true;}
}
function fit(){const list=objects.filter(o=>o.visible);if(list.length)aim(boxOf(list));}
function matches(i){const p=rows[i];return (!$('groupFilter').value||p.group===$('groupFilter').value)&&(!$('subFilter').value||p.subgroup===$('subFilter').value)&&($('back').checked||p.group!=='B01');}
function arrange(){
 const list=objects.filter((o,i)=>matches(i)),spread=$('spreadParts').checked,a=$('exploded').checked?+$('explodeAmount').value:0;
 const cols=Math.ceil(Math.sqrt(list.length)),w=Math.max(100,...list.map(o=>o.userData.size.x))+100,h=Math.max(100,...list.map(o=>o.userData.size.z))+100;
 objects.forEach((o,i)=>{o.visible=matches(i);o.position.copy(o.userData.base).addScaledVector(new THREE.Vector3(...offsets[rows[i].group]),a);});
 if(spread)list.forEach((o,k)=>o.position.copy(o.userData.base).add(new THREE.Vector3((k%cols-(cols-1)/2)*w,0,(Math.floor(k/cols)+.5)*h).sub(o.userData.center)));
 grid.visible=!spread&&!$('groupFilter').value;updateCount();
}
function choose(i){chosen=i;$('partlist').value=String(i);objects.forEach((o,k)=>o.material.emissive.setHex(k===i?0x665017:0));
 const p=rows[i];$('partinfo').textContent=p?`${p.id}｜${groups[p.group]} / ${p.subgroup} [推定]｜材質：未指定（型錄為梣木／橡木選項）｜X ${p.x_mm} × Y ${p.y_mm} × Z ${p.z_mm} mm｜來源 UUID ${p.uuid}`:'全部來源分件；未選取單件';
 $('groupParts').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.i===i)));
}
function updateCount(){$('groupCount').textContent=`目前 ${objects.filter(o=>o.visible).length} 個來源分件／總計 ${objects.length} 個；不是製造／採購件數。`;}
function fill(){const sel=$('partlist');sel.replaceChildren(new Option('全部分件','-1'));$('groupParts').replaceChildren();rows.forEach((p,i)=>{if(!matches(i))return;sel.add(new Option(`${p.id} · ${p.subgroup}`,i));const b=document.createElement('button');b.textContent=p.id;b.dataset.i=i;b.title=p.subgroup;b.onclick=()=>choose(i);$('groupParts').append(b);});choose(-1);arrange();fit();}
function groupChange(){const sf=$('subFilter');sf.replaceChildren(new Option('全部細部分組',''));[...new Set(rows.filter(p=>!$('groupFilter').value||p.group===$('groupFilter').value).map(p=>p.subgroup))].forEach(s=>sf.add(new Option(s,s)));fill();}
function viewBox(id){let b=overall.clone();if(id==='detail')b=boxOf(objects.filter((o,i)=>rows[i].group==='F01'&&rows[i].subgroup==='前腳曲面'));if(id==='handles')b=boxOf(objects.filter((o,i)=>rows[i].group==='F01'&&rows[i].subgroup==='扶手曲面'));return b.isEmpty()?overall:b;}
const directions={persp:[-1,-1.8,.9],front:[0,-1,0],side:[-1,0,0],top:[0,-.0001,1],detail:[-1,-2,.7],handles:[-1,-2,1],bottom:[1,-1,-1]};
function view(id){if(!ready||!objects.some(o=>o.visible))return;aim($('exploded').checked||$('spreadParts').checked||$('groupFilter').value?boxOf(objects.filter(o=>o.visible)):viewBox(id),new THREE.Vector3(...directions[id]));grid.visible=id!=='bottom'&&!$('spreadParts').checked;
 $('referenceImage').src=snapshots[id];$('imageLink').href=snapshots[id];$('imageTitle').textContent=viewNames[id]+' · 原始 CAD 底圖';}
function drawTags(){const used=[];objects.forEach((o,i)=>{const el=tags[i];el.hidden=true;if(!o.visible||!$('partLabels').checked||!($('groupFilter').value||$('subFilter').value||$('spreadParts').checked||chosen===i))return;const p=o.userData.center.clone().add(o.position.clone().sub(o.userData.base)).project(camera);if(p.z< -1||p.z>1)return;let x=(p.x+1)*root.clientWidth/2,y=(1-p.y)*root.clientHeight/2;if(x<0||x>root.clientWidth||y<0||y>root.clientHeight)return;while(used.some(v=>Math.abs(v[0]-x)<46&&Math.abs(v[1]-y)<23))y+=23;if(y>root.clientHeight-24)return;used.push([x,y]);el.hidden=false;el.style.left=`${Math.min(x,root.clientWidth-55)}px`;el.style.top=`${y}px`;});}
const resize=()=>{renderer.setSize(root.clientWidth,root.clientHeight);camera.aspect=root.clientWidth/root.clientHeight;camera.updateProjectionMatrix();if(ready)fit();};new ResizeObserver(resize).observe(root);resize();
const loader=new Rhino3dmLoader();loader.setLibraryPath('https://cdn.jsdelivr.net/npm/rhino3dm@8.17.0/');
loader.load('mc10_clerici_lounge.3dm',model=>{
 model.updateMatrixWorld(true);const source=[];model.traverse(o=>{if(o.isMesh)source.push(o);});source.sort((a,b)=>(a.userData.attributes?.id||'').localeCompare(b.userData.attributes?.id||''));
 source.forEach((o,i)=>{const geometry=o.geometry.clone().applyMatrix4(o.matrixWorld),mesh=new THREE.Mesh(geometry);const b=new THREE.Box3().setFromBufferAttribute(geometry.attributes.position),c=b.getCenter(new THREE.Vector3()),s=b.getSize(new THREE.Vector3()),[group,subgroup]=classify(c,s);mesh.material=new THREE.MeshStandardMaterial({color:colors[group],roughness:.6,side:THREE.DoubleSide});mesh.userData={base:new THREE.Vector3(),center:c,size:s};scene.add(mesh);objects.push(mesh);rows.push({id:`M${String(i+1).padStart(3,'0')}`,group,subgroup,uuid:o.userData.attributes?.id||'',x_mm:+s.x.toFixed(3),y_mm:+s.y.toFixed(3),z_mm:+s.z.toFixed(3),material:'未指定',status:'DERIVED mesh AABB; grouping ASSUMED'});const tag=document.createElement('button');tag.className='partTag';tag.textContent=rows[i].id;tag.onclick=()=>choose(i);$('partOverlay').append(tag);tags.push(tag);});
 overall=boxOf(objects);grid.position.x=overall.getCenter(new THREE.Vector3()).x;grid.position.y=overall.getCenter(new THREE.Vector3()).y;
 makeImages();const gf=$('groupFilter');gf.add(new Option('全部 GROUP',''));Object.entries(groups).forEach(([k,v])=>gf.add(new Option(`${k} · ${v}`,k)));ready=true;groupChange();view('persp');$('status').textContent='來源 CAD · D02 · 可旋轉／雙擊分件';
 const fields=Object.keys(rows[0]);const csv='\uFEFF'+[fields.join(','),...rows.map(p=>fields.map(k=>'"'+String(p[k]).replaceAll('"','""')+'"').join(','))].join('\r\n');$('csv').href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
 const report=new URLSearchParams(location.search).get('report');if(report)reportPage(report);document.body.dataset.ready='true';
},undefined,error=>{$('status').textContent='模型載入失敗，請重新整理或下載原始 3DM';console.error(error);});
// Independent renderer: fixed gallery images never follow interaction or explosion.
let photoRenderer;
function makeImages(){photoRenderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});photoRenderer.setSize(800,600);const c=new THREE.PerspectiveCamera(35,4/3,1,100000);c.up.set(0,0,1);grid.visible=false;Object.keys(viewNames).forEach(id=>{aim(viewBox(id),new THREE.Vector3(...directions[id]),c);photoRenderer.render(scene,c);snapshots[id]=photoRenderer.domElement.toDataURL('image/png');});grid.visible=true;}
function reportPage(type){const host=$('reports');host.hidden=false;const h=document.createElement('h2');h.textContent=type==='atlas'?'來源分件圖冊 · 非製造零件圖':'尺寸與數量驗證 · 非製造認證';host.append(h);const p=document.createElement('p');const size=overall.getSize(new THREE.Vector3());p.textContent=`來源網格 ${rows.length} 件；UUID 唯一 ${new Set(rows.map(p=>p.uuid)).size} 件；全部已分類。網格 AABB X/Y/Z = ${size.toArray().map(v=>v.toFixed(3)).join(' × ')}。型錄 655 × 840 × 700 mm；X/Y 次序不同，誤差及來源單位仍待核對。`;host.append(p);
 if(type==='atlas'){const gallery=document.createElement('div');gallery.className='atlas';host.append(gallery);grid.visible=false;objects.forEach(o=>o.visible=false);const c=new THREE.PerspectiveCamera(35,4/3,1,100000);c.up.set(0,0,1);objects.forEach((o,i)=>{o.visible=true;aim(boxOf([o]),new THREE.Vector3(-1,-1.8,1),c);photoRenderer.render(scene,c);const article=document.createElement('article'),img=document.createElement('img'),label=document.createElement('p');img.src=photoRenderer.domElement.toDataURL('image/png');img.alt=rows[i].id+' 來源幾何';label.textContent=`${rows[i].id} · ${rows[i].group} / ${rows[i].subgroup}｜${rows[i].x_mm} × ${rows[i].y_mm} × ${rows[i].z_mm}（來源座標）`;article.append(img,label);gallery.append(article);o.visible=false;});arrange();}
 else{const table=document.createElement('table');const tr=document.createElement('tr');['ID','GROUP（推定）','細部分組（推定）','X','Y','Z','來源 UUID'].forEach(v=>{const th=document.createElement('th');th.textContent=v;tr.append(th);});table.append(tr);rows.forEach(p=>{const tr=document.createElement('tr');[p.id,p.group,p.subgroup,p.x_mm,p.y_mm,p.z_mm,p.uuid].forEach(v=>{const td=document.createElement('td');td.textContent=v;tr.append(td);});table.append(tr);});host.append(table);}host.scrollIntoView();}
Object.entries(viewNames).forEach(([id,name])=>{$(id).onclick=()=>view(id);const b=document.createElement('button');b.textContent=name;b.onclick=()=>view(id);$('galleryButtons').append(b);});
$('groupFilter').onchange=groupChange;$('subFilter').onchange=fill;$('back').onchange=fill;$('partlist').onchange=()=>choose(+$('partlist').value);
['spreadParts','exploded'].forEach(id=>$(id).onchange=()=>{arrange();fit();});$('explodeAmount').oninput=()=>{arrange();fit();};$('wire').onchange=()=>objects.forEach(o=>o.material.wireframe=$('wire').checked);
const ray=new THREE.Raycaster();renderer.domElement.addEventListener('dblclick',e=>{const r=renderer.domElement.getBoundingClientRect();ray.setFromCamera(new THREE.Vector2((e.clientX-r.left)/r.width*2-1,1-(e.clientY-r.top)/r.height*2),camera);const hit=ray.intersectObjects(objects.filter(o=>o.visible))[0];if(hit)choose(objects.indexOf(hit.object));});
renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera);if(ready)drawTags();});

$('enlarge').onclick=()=>{$('largeImage').src=$('referenceImage').src;$('imageDialog').showModal();};$('closeImage').onclick=()=>$('imageDialog').close();
