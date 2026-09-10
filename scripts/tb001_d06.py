#!/usr/bin/env python3
"""D06: D04 laminated legs, D05 tray envelopes, load-bearing line clusters.
Nominal joinery / exterior proposal; no strength certification.
"""
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
COLORS = {'WALNUT':'#63432e', 'MAPLE':'#e5d6b5'}
VIEWS = {
    'persp': {'label':'透視', 'position':[-1.1,-1.7,1.25], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.87},
    'front': {'label':'正面', 'position':[.3,-2,.3], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.76},
    'side': {'label':'左側', 'position':[-2,.24,.3], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.76},
    'top': {'label':'俯視', 'position':[.3,.24,3], 'target':[.3,.24,.3], 'up':[0,1,0], 'span':.68},
    'detail': {'label':'承托與半搭接', 'position':[-.40,-.65,.48], 'target':[.048,.086,.292], 'up':[0,0,1], 'span':.27},
    'bottom': {'label':'底部', 'position':[-1.1,-1.7,-1.0], 'target':[.3,.24,.3], 'up':[0,0,1], 'span':.90},
}

def polygon(x,y,w,d,c):
    return [(x+c,y),(x+w-c,y),(x+w,y+c),(x+w,y+d-c),
            (x+w-c,y+d),(x+c,y+d),(x,y+d-c),(x,y+c)]


def add(name,group,mat,x,y,z,w,d,h,role):
    base.box(name,group,mat,x,y,z,w,d,h)
    base.PARTS[-1]['role']=role


def build(line_count=None):
    line_count=P['support_line_count'] if line_count is None else line_count
    assert line_count in (1,2)
    base.P=P; base.OUT=OUT; base.REV='D06'; base.COLORS=COLORS; base.PARTS=[]
    secondary=[(-40,-30)] if line_count==2 else []
    # D04 8/14/8 laminated leg section and 22 mm feet. Move the posts 2/8 mm
    # outwards so D05's EXACT tray envelopes fit without corner penetration.
    xs=[18,552];ys=[12,428];core_x=[26,560]
    slots=[]
    for bottom in [74,320]:
        slots += [(bottom+a,bottom+b) for a,b in secondary]+[(bottom-18,bottom)]
    for ix,x in enumerate(xs):
        for iy,y in enumerate(ys):
            name=f'Leg {ix+1}{iy+1}'
            add(name+' walnut foot','Legs','WALNUT',x,y,0,30,40,22,'foot')
            for dx in [0,22]:add(name+' walnut cheek','Legs','WALNUT',x+dx,y,22,8,40,554,'leg_cheek')
            start=22
            for lo,hi in slots+[(576,576)]:
                if lo>start:add(name+' maple core','Legs','MAPLE',x+8,y,start,14,40,lo-start,'leg_core')
                start=hi
    # One main bearer plus an optional single, separated bracing line.
    # Both project 10 mm beyond the leg faces and pass through actual core slots.
    for group,bottom in [('Lower',74),('Middle',320)]:
        z=bottom-18; lap=z+9
        for x in core_x:
            for start,stop in [(bottom+a,bottom+b) for a,b in secondary]:
                add(group+' through bracing line',group,'WALNUT',x,2,start,14,476,stop-start,'through_brace')
            add(group+' main side bearer lower half',group,'WALNUT',x,2,z,14,476,9,'side_bearer')
            for y0,y1 in [(2,76),(104,376),(404,478)]:
                add(group+' main side bearer upper half',group,'WALNUT',x,y0,lap,14,y1-y0,9,'side_bearer')
        for y in [76,376]:
            add(group+' transverse bearer lower half',group,'WALNUT',40,y,z,520,28,9,'cross_bearer')
            add(group+' transverse bearer upper half',group,'WALNUT',26,y,lap,548,28,9,'cross_bearer')
    # Original D05 top apron placement now follows the straight D04 posts.
    for y in [23,439]:add('Top front/back apron','Top','WALNUT',48,y,552,504,18,24,'apron')
    for x in [24,558]:add('Top side apron','Top','WALNUT',x,52,552,18,376,24,'apron')
    # Exact D05 outer base and raised-panel geometry, but NOT a solid dark slab:
    # eight mitred perimeter pieces enclose a plywood infill of equal thickness.
    reference=json.loads((OUT.parent/'D05/geometry_mm.json').read_text())['parts']
    for group in ['Lower','Middle','Top']:
        oldbase=next(p for p in reference if p['group']==group and ('tray base' in p['name'] or 'top base' in p['name']))
        x,y,z=oldbase['origin_mm'];w,d,h=oldbase['size_mm'];c=24 if group=='Top' else 14
        outer=polygon(x,y,w,d,c);e=P['top_edge_width'] if group=='Top' else P['shelf_edge_width'];inner=polygon(x+e,y+e,w-2*e,d-2*e,max(4,c-4))
        for i in range(8):
            j=(i+1)%8
            d05.poly_prism(group+f' mitred perimeter strip {i+1}',group,'WALNUT',[outer[i],outer[j],inner[j],inner[i]],z,h)
            base.PARTS[-1]['role']='perimeter_strip'
        d05.poly_prism(group+' plywood infill',group,'MAPLE',inner,z,h)
        base.PARTS[-1]['role']='plywood_core'
        old=next(p for p in reference if p['group']==group and 'inset' in p['name'])
        part=json.loads(json.dumps(old));part['id']=f'P{len(base.PARTS)+1:03}'
        part['name']=group+' maple-veneered plywood raised panel';part['role']='raised_panel';part['material']='MAPLE'
        base.PARTS.append(part)


def contact(a,b):
    # All structural contacts are axis-aligned rectangles (the tray's inset is
    # checked separately). Edge/point contact is deliberately not accepted.
    aa=np.array(a['vertices_mm']);bb=np.array(b['vertices_mm'])
    ext=np.minimum(aa.max(0),bb.max(0))-np.maximum(aa.min(0),bb.min(0))
    return sum(abs(ext)<1e-7)==1 and sum(ext>1e-7)==2


def volume(p):
    vv=np.array(p['vertices_mm']);total=0
    for f in p['faces']:
        for i in range(1,len(f)-1):total+=np.dot(vv[f[0]],np.cross(vv[f[i]],vv[f[i+1]]))/6
    return abs(total)


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
    for group in ['Lower','Middle','Top']:
        old=next(p for p in reference if p['group']==group and 'inset' in p['name'])
        now=next(p for p in base.PARTS if p['group']==group and p['role']=='raised_panel')
        assert now['vertices_mm']==old['vertices_mm'] and now['faces']==old['faces']
        oldbase=next(p for p in reference if p['group']==group and ('tray base' in p['name'] or 'top base' in p['name']))
        deck=[p for p in base.PARTS if p['group']==group and p['role'] in ['perimeter_strip','plywood_core']]
        assert np.isclose(sum(volume(p) for p in deck),volume(oldbase))
        core=next(p for p in deck if p['role']=='plywood_core')
        outline=np.array(now['vertices_mm'][:len(now['vertices_mm'])//2])[:,:2]
        for point in np.array(core['vertices_mm'])[:,:2]:
            for a,b in zip(outline,np.roll(outline,-1,axis=0)):
                e=b-a;v=point-a
                assert e[0]*v[1]-e[1]*v[0]>=-1e-7, 'Pale core exposed outside raised panel'

    collisions=[[a['id'],b['id']] for a,b in itertools.combinations(base.PARTS,2) if overlap(a,b)]
    assert not collisions,collisions
    for p in base.PARTS:
        edges={}
        for f in p['faces']:
            for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted([a,b])),[]).append((a,b))
        assert all(len(v)==2 and v[0]==v[1][::-1] for v in edges.values())
    vv=np.array([v for p in base.PARTS for v in p['vertices_mm']])
    assert np.allclose(vv.min(0),[0,0,0]) and np.allclose(vv.max(0),[600,480,600])
    paths={}
    for group,bottom in [('Lower',74),('Middle',320)]:
        bearers=[p for p in base.PARTS if p['group']==group and p['role']=='cross_bearer' and p['origin_mm'][2]==bottom-9]
        panel=next(p for p in base.PARTS if p['group']==group and p['role']=='plywood_core')
        sides=[p for p in base.PARTS if p['group']==group and p['role']=='side_bearer' and p['origin_mm'][2]==bottom-18]
        cores=[p for p in base.PARTS if p['role']=='leg_core']
        assert len(bearers)==2 and all(contact(p,panel) for p in bearers)
        assert all(sum(contact(b,s) for s in sides)==2 for b in bearers)
        assert all(sum(contact(s,c) for c in cores)==2 for s in sides)
        paths[group]={'panel':panel['id'],'cross_bearers':[p['id'] for p in bearers],
                      'side_bearers':[p['id'] for p in sides],
                      'path':'plywood deck -> two transverse bearers -> half-laps -> through side bearers -> maple core slot shoulders -> laminated legs -> feet',
                      'verified':'positive-area bearing contact, NOT strength or joint sizing'}
    old_volume=sum(volume(p) for p in reference if 'tray base' in p['name'] or 'top base' in p['name'])
    rim_volume=sum(volume(p) for p in base.PARTS if p['role']=='perimeter_strip')
    return dict(part_count=len(base.PARTS),d05_raised_panels_unchanged=3,d04_leg_section_mm=[8,14,8],
        bounds_mm=[[0,600],[0,480],[0,600]],positive_volume_overlap=collisions,
        closed_consistently_wound_meshes=True,load_paths=paths,
        dark_deck_material_mm3={'previous_solid_bases':old_volume,'new_perimeter_only':rim_volume,
            'volume_reduction_percent':round(100*(1-rim_volume/old_volume),1),'note':'net model volume only, not purchase quantity or total cost'},
        surface_heights_mm=P['surface_levels'],maturity='L1',engineering_verified=False,
        note='Nominal slots/half-laps and positive-area bearing are modelled. Adhesives, mechanical retention, tolerances, plywood specification, strength and racking remain unverified.')


def viewer(data):
    # The D05 document is the baseline UI, not the rejected D06 viewer.
    html=(OUT.parent/'D05/TB001_D05_viewer.html').read_text()
    html=re.sub(r'const data=.*?;window.tb001Data=data;',lambda _: 'const data='+json.dumps(data,separators=(',',':'))+';window.tb001Data=data;',html)
    html=html.replace('const controls=new OrbitControls','let controls=new OrbitControls')
    html=html.replace('D05','D06').replace('QUIET FRAME','QUIET FRAME / LIGHT RHYTHM').replace('Quiet Frame 三層邊几','Quiet Frame · Light Rhythm')
    html=html.replace('降低線條密度，以錐形單體腿、柔角托盤面及單一道後撐建立偏歐美的 Japandi。','D04 三明治腳 × D05 托盤輪廓。每側兩道線，12 mm 留白，端頭穿出腳外 10 mm。主承托保留；楓木面＋四周胡桃木條，不用整片胡桃木底板。')
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
    html=re.sub(r'const colors=\{.*?\};', 'const colors={WALNUT:0x63432e,MAPLE:0xe5d6b5};',html)
    html=html.replace('煙燻橡木單體錐形腿；自然橡木嵌面。','胡桃木／楓木三明治腳；胡桃木條收邊；乳白楓木貼皮夾板面。').replace('煙燻橡木框架','胡桃木條托架／收邊').replace('自然橡木嵌面','楓木貼皮夾板面')
    html=html.replace('榫接、面板托持與木材活動量待確認，尚未驗證承重。','已建立名義承托與半搭接；公差、固定方式、承重及側向剛性仍待驗證。')
    html=html.replace('#594638','#63432e').replace('#c8aa7d','#e5d6b5')
    html=html.replace('<label>分層展開', '<p><label><input type="checkbox" id="showSupports"> 移除托盤，查看承托</label></p><p><a href="construction.html">一條／兩條比較與承托 →</a></p><label>分層展開')
    html=html.replace("select.onchange=()=>choose(select.value);", "select.onchange=()=>choose(select.value);document.querySelector('#showSupports').onchange=e=>{objects.forEach((o,i)=>{o.visible=!(e.target.checked&&['raised_panel','plywood_core','perimeter_strip'].includes(data.parts[i].role));});choose('');};")
    html=html.replace('ray.intersectObjects(objects)[0]', 'ray.intersectObjects(objects.filter(o=>o.visible))[0]')
    html=html.replace("+' 個視覺分件'", "+' 個網格區塊（非加工件數）'")
    html=html.replace('<small>TB001 / D06', '<small><a href="../">← 總覽</a> · TB001 / D06')
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
