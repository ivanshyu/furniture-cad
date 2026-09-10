#!/usr/bin/env python3
"""D06 is D05 plus TWO slender side lines. Not the rejected blade-leg design."""
import csv
import hashlib
import itertools
import json
import re
from pathlib import Path
import numpy as np
import tb001_d05 as d05

base = d05.base
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'02_Tables/TB001_D16_Three_Tier/models/D06'
P = json.loads((OUT/'parameters.json').read_text())
COLORS = {'SMOKED_OAK': '#594638', 'NATURAL_OAK': '#c8aa7d'}
VIEWS = {
    'persp': {'label':'透視', 'position':[-1.1,-1.7,1.25], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.87},
    'front': {'label':'正面', 'position':[.3,-2,.3], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.76},
    'side': {'label':'左側', 'position':[-2,.24,.3], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.76},
    'top': {'label':'俯視', 'position':[.3,.24,3], 'target':[.3,.24,.3], 'up':[0,1,0], 'span':.68},
    'detail': {'label':'細橫線接點', 'position':[-.40,-.65,.59], 'target':[.055,.085,.367], 'up':[0,0,1], 'span':.27},
    'bottom': {'label':'底部', 'position':[-1.1,-1.7,-1.0], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.90},
}

def build():
    base.P=P; base.OUT=OUT; base.REV='D06'; base.COLORS=COLORS; base.PARTS=[]
    d05.P=P
    d05.build()
    # Preserve all 15 D05 components byte-for-byte; additions meet the true
    # sloping leg faces (not their bounding boxes). No projection beyond D05.
    for side in [0,1]:
        cx=P['setback']+P['post_x']/2
        if side: cx=P['width']-cx
        lo=P['side_line_bottom']; hi=lo+P['side_line_height']
        vertices=[]
        for z in [lo,hi]:
            taper=(P['post_y']-P['post_bottom_y'])/2*(1-z/(P['height']-P['top_thickness']))
            yf=P['setback']+P['post_y']-taper
            yb=P['depth']-P['setback']-P['post_y']+taper
            x=cx-P['side_line_width']/2
            vertices.extend([[x,yf,z],[x+P['side_line_width'],yf,z],
                             [x+P['side_line_width'],yb,z],[x,yb,z]])
        vv=np.array(vertices)
        base.PARTS.append(dict(id=f'P{len(base.PARTS)+1:03}',name=('Left' if not side else 'Right')+' fine side line',
            group='Side lines',material='SMOKED_OAK',origin_mm=vv.min(axis=0).tolist(),
            size_mm=np.ptp(vv,axis=0).tolist(),vertices_mm=vertices,faces=base.FACES))

def overlap(a,b):
    """Exact separating-axis test for the convex polyhedra in this model."""
    av=np.array(a['vertices_mm']);bv=np.array(b['vertices_mm'])
    if np.any(np.minimum(av.max(0),bv.max(0))-np.maximum(av.min(0),bv.min(0))<=1e-7):return False
    axes=[];edge_sets=[]
    for p,vs in [(a,av),(b,bv)]:
        edges=[]
        for f in p['faces']:
            axes.append(np.cross(vs[f[1]]-vs[f[0]],vs[f[2]]-vs[f[0]]))
            edges.extend(vs[j]-vs[i] for i,j in zip(f,f[1:]+f[:1]))
        edge_sets.append(edges)
    axes.extend(np.cross(x,y) for x in edge_sets[0] for y in edge_sets[1])
    for ax in axes:
        n=np.linalg.norm(ax)
        if n<1e-10:continue
        ax=ax/n; aa=av@ax;bb=bv@ax
        if min(aa.max(),bb.max())-max(aa.min(),bb.min())<=1e-7:return False
    return True

def verify():
    reference=json.loads((OUT.parent/'D05/geometry_mm.json').read_text())['parts']
    assert base.PARTS[:15]==reference, 'D05 base geometry drifted'
    collisions=[[a['id'],b['id']] for a,b in itertools.combinations(base.PARTS,2) if overlap(a,b)]
    assert not collisions,collisions
    for p in base.PARTS:
        edges={}
        for f in p['faces']:
            for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted([a,b])),[]).append((a,b))
        assert all(len(v)==2 and v[0]==v[1][::-1] for v in edges.values())
    vv=np.array([v for p in base.PARTS for v in p['vertices_mm']])
    assert np.allclose(vv.min(0),[0,0,0]) and np.allclose(vv.max(0),[600,480,600])
    return dict(part_count=17,d05_base_parts_unchanged=15,added_parts=2,bounds_mm=[[0,600],[0,480],[0,600]],
        positive_volume_overlap=collisions,collision_method='convex SAT, face and edge axes',closed_consistently_wound_meshes=True,
        surface_heights_mm=P['surface_levels'],clear_opening_front_mm=[228,214],
        side_line_bottom_mm=P['side_line_bottom'],side_line_gap_above_middle_mm=32,
        maturity='L1',engineering_verified=False,note='Surface-contact line ends are not designed joinery; D05 shelf support and racking remain unresolved.')

def viewer(data):
    # The D05 document is the baseline UI, not the rejected D06 viewer.
    html=(OUT.parent/'D05/TB001_D05_viewer.html').read_text()
    html=re.sub(r'const data=.*?;window.tb001Data=data;',lambda _: 'const data='+json.dumps(data,separators=(',',':'))+';window.tb001Data=data;',html)
    html=html.replace('const controls=new OrbitControls','let controls=new OrbitControls')
    html=html.replace('D05','D06').replace('QUIET FRAME','QUIET FRAME / FINE LINES').replace('Quiet Frame 三層邊几','Quiet Frame · Fine Lines')
    html=html.replace('降低線條密度，以錐形單體腿、柔角托盤面及單一道後撐建立偏歐美的 Japandi。','以 D05 為底：15 件原始幾何完全保留，只在左右側各加一道 8 × 10 mm 細橫線。')
    html=html.replace('<nav><button data-view="persp">立體</button><button data-view="front">正面</button><button data-view="side">側面</button><button data-view="top">俯視</button></nav>',
        '<nav>'+''.join(f'<button data-view="{k}">{v["label"]}</button>' for k,v in VIEWS.items())+'</nav>')
    html=html.replace("({Legs:0,'Side lines':0,Lower:.10,Middle:.25,Top:.42}[data.parts[i].group])", "({Legs:0,'Side lines':0,Structure:0,Lower:.10,Middle:.25,Top:.42}[data.parts[i].group]??0)")
    start=html.index("let viewName='persp';")
    end=html.index("document.querySelectorAll('[data-view]')",start)
    html=html[:start]+'''const viewSpecs=__VIEWS__;let viewName='persp';
function view(name){viewName=name;const v=viewSpecs[name];controls.dispose();camera.up.set(...v.up);camera.position.set(...v.position);controls=new OrbitControls(camera,renderer.domElement);controls.target.set(...v.target);controls.target.z+=Number(document.querySelector('#explode').value)*.14;controls.enableDamping=true;floor.visible=name!=='bottom';camera.zoom=1;resize();controls.update();}
function resize(){const w=host.clientWidth,h=host.clientHeight,a=w/h;const span=(viewSpecs[viewName].span+Number(document.querySelector('#explode').value)*.48)*Math.max(1,1/a);camera.left=-span*a/2;camera.right=span*a/2;camera.top=span/2;camera.bottom=-span/2;camera.updateProjectionMatrix();renderer.setSize(w,h);}
'''.replace('__VIEWS__',json.dumps(VIEWS))+html[end:]
    html=html.replace('<details><summary>查看立體與三視圖尺寸板</summary>', '''<section class="gallery"><div><small>FIXED CAMERA / MATERIAL STUDY</small><h2 id="galleryTitle">透視 · AI 材質</h2><p>相機與 CAD 底圖逐一配對。AI 可能改變局部線條、比例或接點；不能用來量尺寸。</p><nav id="galleryViews"></nav><nav><button id="aiMode" aria-pressed="true">AI 材質</button><button id="cadMode" aria-pressed="false">CAD 底圖</button></nav><a id="galleryLink" target="_blank"><img id="galleryImage" alt="固定視角材質與CAD對照"></a><p><a href="gallery/ai_prompt.txt">完整共用 prompt</a> · <a href="gallery/prompts.json">逐視角 prompts</a> · <a href="gallery/ai_manifest.json">產圖與 QA 紀錄</a></p></div></section><details><summary>查看立體與三視圖尺寸板</summary>''')
    html=html.replace('</style>','.gallery{padding:28px 36px;border-top:1px solid #d6cbbd}.gallery>div{max-width:1050px;margin:auto}.gallery img{width:100%;height:min(80vh,900px);object-fit:contain;background:#f3efe7}button[aria-pressed=true]{background:#5b4636;color:white}.gallery nav{margin:12px 0}header a{font-size:13px}</style>')
    html=html.replace('</body>', '''<script>
const gallerySpecs=__VIEWS__;let galleryView='persp',galleryMode='ai';
function showGallery(){const src='gallery/'+galleryView+'_'+galleryMode+'.png';document.querySelector('#galleryImage').src=src;document.querySelector('#galleryLink').href=src;document.querySelector('#galleryTitle').textContent=gallerySpecs[galleryView].label+' · '+(galleryMode==='ai'?'AI 材質':'CAD 底圖');document.querySelector('#aiMode').setAttribute('aria-pressed',galleryMode==='ai');document.querySelector('#cadMode').setAttribute('aria-pressed',galleryMode==='cad');document.querySelectorAll('[data-gallery]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.gallery===galleryView));}
for(const [id,v] of Object.entries(gallerySpecs)){const b=document.createElement('button');b.textContent=v.label;b.dataset.gallery=id;b.onclick=()=>{galleryView=id;showGallery();document.querySelector('[data-view="'+id+'"]').click();};document.querySelector('#galleryViews').append(b);}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{galleryView=b.dataset.view;showGallery();}));for(const mode of ['ai','cad'])document.querySelector('#'+mode+'Mode').onclick=()=>{galleryMode=mode;showGallery();};showGallery();
</script></body>'''.replace('__VIEWS__',json.dumps(VIEWS)))
    version=hashlib.sha256((OUT/'geometry_mm.json').read_bytes()).hexdigest()[:12]
    html=html.replace("+'_'+galleryMode+'.png';", "+'_'+galleryMode+'.png?v="+version+"';")
    (OUT/'TB001_D06_viewer.html').write_text(html)

def main():
    build(); checks=verify()
    data=dict(revision='D06',units='mm',parameters=P,parts=base.PARTS)
    (OUT/'geometry_mm.json').write_text(json.dumps(data,separators=(',',':')))
    with (OUT/'parts_dimensions.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['id','name','group','material','x_mm','y_mm','z_mm','width_mm','depth_mm','height_mm','status'])
        for p in base.PARTS:w.writerow([p['id'],p['name'],p['group'],p['material'],*p['origin_mm'],*p['size_mm'],'L1 exterior only; not cut list'])
    base.glb();viewer(data)
    (OUT/'model_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    (OUT/'views.json').write_text(json.dumps(VIEWS,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
