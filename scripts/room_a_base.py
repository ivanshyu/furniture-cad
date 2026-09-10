#!/usr/bin/env python3
"""Room A concept model: mm source geometry, metre/Y-up GLB, plan and viewer."""
import json
import math
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '04_Rooms/RA001_Bedroom_A/models/BASE01'
P = json.loads((OUT / 'parameters.json').read_text())
PARTS = []
COLORS = {'wall':'#e5e1d9','floor':'#c7b49a','cabinet':'#d5c7ae','wood':'#906a46','linen':'#e6e3d9','glass':'#9fbdc1','trim':'#b8b4a9'}
FACES = [[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]

def box(name, group, material, x,y,z,w,d,h,status='ASSUMED'):
    assert min(w,d,h)>0, name
    PARTS.append(dict(name=name,group=group,material=material,origin_mm=[x,y,z],size_mm=[w,d,h],status=status,
        vertices_mm=[[x,y,z],[x+w,y,z],[x+w,y+d,z],[x,y+d,z],[x,y,z+h],[x+w,y,z+h],[x+w,y+d,z+h],[x,y+d,z+h]]))

def build():
    r=P['room']; c=P['wardrobe']; b=P['bed']; n=P['window']; q=P['boxing']
    W,D,H,T=r['foot_wall'],r['depth'],r['height'],r['wall_thickness']; X=W-r['head_wall']; Y=r['notch_depth']
    box('睡眠區地板','Floor','floor',X,0,-60,W-X,D,60,'DERIVED')
    box('入口延伸地板','Floor','floor',0,Y,-60,X,D-Y,60)
    box('床頭牆 315 cm','Walls','wall',X,-T,0,W-X,T,H,'DERIVED')
    box('衛浴右隔間','Walls','wall',X-T,0,0,T,Y,H)
    box('衛浴下隔間／門洞待補','Walls','wall',0,Y-T,0,X-T,T,H)
    box('床尾牆 550 cm','Cutaway','wall',0,D,0,W,T,H,'DERIVED')
    door=P['entrance']['width']; opening=D-door
    box('入口側牆','Cutaway','wall',-T,Y,0,T,opening-Y,H)
    box('入口門楣（暫定）','Cutaway','wall',-T,opening,2100,T,door,H-2100)
    wy,ww,ws,wh=n['offset_from_head'],n['width'],n['sill'],n['height']
    box('窗側前牆','Walls','wall',W,0,0,T,wy,H)
    box('窗側後牆','Walls','wall',W,wy+ww,0,T,D-wy-ww,H)
    box('窗台下牆','Walls','wall',W,wy,0,T,ww,ws)
    box('窗上牆','Walls','wall',W,wy,ws+wh,T,ww,H-ws-wh)
    box('窗開口佔位（尺寸待量）','Window','glass',W+T/2,wy,ws,12,ww,wh)
    for i in range(30):
        box('百葉示意','Window','trim',W-8,wy,ws+i*wh/30,10,ww,10)
    box('冷氣側包管 · 下垂40／突出11 cm','Boxing','wall',q['start_x'],D-q['projection'],H-q['drop'],q['end_x']-q['start_x'],q['projection'],q['drop'],'DERIVED')
    box('頂天系統櫃 211.4×60×248.5 cm','Wardrobe','cabinet',X,0,0,c['depth']-20,c['length'],c['height'],'KNOWN')
    # Simplified elevation divisions; curved field-cut infill remains unresolved.
    segments=[428,428,427,381,382]; off=18
    for i,width in enumerate(segments):
        box(f'衣櫃下門板{i+1}（分件示意）','Wardrobe','cabinet',X+c['depth']-20,off,10,20,width-3,H-480)
        box(f'衣櫃上區{i+1}（收邊待核）','Wardrobe','cabinet',X+c['depth']-20,off,H-470,20,width-3,460)
        off+=width
    bx=W-b['right_gap']-b['width']; total=b['total_depth']; hd=b['headboard_depth']
    box('木床頭佔位','Bed','wood',bx,0,0,b['width'],hd,b['headboard_height'])
    box('木床架佔位','Bed','wood',bx,hd,0,b['width'],total-hd,b['base_height'])
    box('床墊佔位','Bed','linen',bx+20,hd+10,b['base_height'],b['width']-40,total-hd-30,b['mattress_height'])
    for dx in [100,b['width']/2+50]:
        box('枕頭佔位','Bed','linen',bx+dx,hd+50,b['base_height']+b['mattress_height'],b['width']/2-170,400,80)
    box('睡眠區天花板','Ceiling','wall',X,0,H,W-X,D,60,'DERIVED')
    box('入口天花板','Ceiling','wall',0,Y,H,X,D-Y,60)

def export_glb():
    binary=bytearray(); views=[]; accessors=[]; meshes=[]; nodes=[]
    for part in PARTS:
        vv=[[x/1000,z/1000,-y/1000] for x,y,z in part['vertices_mm']]; pos=[]; norm=[]
        for f in FACES:
            a=[vv[f[1]][k]-vv[f[0]][k] for k in range(3)];b=[vv[f[2]][k]-vv[f[0]][k] for k in range(3)]
            n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]; length=math.sqrt(sum(v*v for v in n)); n=[v/length for v in n]
            for i in [f[0],f[1],f[2],f[0],f[2],f[3]]: pos.extend(vv[i]);norm.extend(n)
        attrs={}
        for kind,values in [('POSITION',pos),('NORMAL',norm)]:
            start=len(binary);binary.extend(struct.pack('<'+'f'*len(values),*values));views.append(dict(buffer=0,byteOffset=start,byteLength=len(values)*4,target=34962))
            acc=dict(bufferView=len(views)-1,componentType=5126,count=len(values)//3,type='VEC3')
            if kind=='POSITION':acc.update(min=[min(values[k::3]) for k in range(3)],max=[max(values[k::3]) for k in range(3)])
            accessors.append(acc);attrs[kind]=len(accessors)-1
        meshes.append(dict(name=part['name'],primitives=[dict(attributes=attrs,material=list(COLORS).index(part['material']))]))
        nodes.append(dict(name=part['name'],mesh=len(meshes)-1,extras=dict(group=part['group'],evidence=part['status'])))
    mats=[dict(name=k,pbrMetallicRoughness=dict(baseColorFactor=[int(c[i:i+2],16)/255 for i in (1,3,5)]+[1],metallicFactor=0,roughnessFactor=.85)) for k,c in COLORS.items()]
    # Default scene cuts away front walls and ceiling; second scene is the complete enclosure.
    visible=[i for i,p in enumerate(PARTS) if p['group'] not in ('Cutaway','Ceiling')]
    data=dict(asset=dict(version='2.0',generator='Room A BASE01'),scene=0,scenes=[dict(name='Cutaway',nodes=visible),dict(name='Full enclosure',nodes=list(range(len(nodes))))],nodes=nodes,meshes=meshes,materials=mats,buffers=[dict(byteLength=len(binary))],bufferViews=views,accessors=accessors)
    raw=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode();raw+=b' '*((-len(raw))%4)
    blob=struct.pack('<III',0x46546c67,2,28+len(raw)+len(binary))+struct.pack('<II',len(raw),0x4e4f534a)+raw+struct.pack('<II',len(binary),0x004e4942)+binary
    (OUT/'room_a.glb').write_bytes(blob)
    check=(OUT/'room_a.glb').read_bytes();assert struct.unpack_from('<I',check,8)[0]==len(check)
    size=struct.unpack_from('<I',check,12)[0];decoded=json.loads(check[20:20+size]);assert len(decoded['nodes'])==len(PARTS)
    assert all(v['byteOffset']+v['byteLength']<=len(binary) for v in decoded['bufferViews'])

def plan():
    r=P['room'];b=P['bed'];c=P['wardrobe']; W=r['foot_wall'];D=r['depth'];X=W-r['head_wall'];Y=r['notch_depth'];bx=W-b['right_gap']-b['width']
    s=.135;ox=95;oy=150
    def xy(x,y):return f'{ox+x*s:.2f},{oy+y*s:.2f}'
    def rect(x,y,w,h,color):return f'<rect x="{ox+x*s}" y="{oy+y*s}" width="{w*s}" height="{h*s}" fill="{color}" stroke="#807b70"/>'
    def label(x,y,text,size=14):return f'<text x="{ox+x*s}" y="{oy+y*s}" font-size="{size}" text-anchor="middle">{text}</text>'
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="760" viewBox="0 0 960 760"><rect width="960" height="760" fill="#f5f2eb"/><g font-family="Arial,PingFang TC,sans-serif" fill="#373c36">',
        '<text x="50" y="48" font-size="15" letter-spacing="3">ROOM A / BASE01</text><text x="50" y="88" font-size="28">房A · 現況空間基準</text>',
        f'<polygon points="{xy(X,0)} {xy(W,0)} {xy(W,D)} {xy(0,D)} {xy(0,Y)} {xy(X,Y)}" fill="#e6dccb" stroke="#585e55" stroke-width="6"/>',
        rect(X,0,c['depth'],c['length'],'#c8b796'),rect(bx,0,b['width'],b['total_depth'],'#a68765'),rect(bx+20,110,b['width']-40,b['total_depth']-130,'#f5f4ed'),
        rect(P['boxing']['start_x'],D-110,P['boxing']['end_x']-P['boxing']['start_x'],110,'#9bad9d'),
        label(X+(W-X)/2,-150,'床頭側 315 cm（含櫃深）'),label(W/2,D+270,'床尾整面 550 cm'),label(bx+b['width']/2,950,'床 · 佔位模型'),label(bx+b['width']/2,1190,f'外形暫採 {b["width"]/10:g} × {b["total_depth"]/10:g} cm',12),
        label(X+300,1050,'系統櫃',13),label(X+300,1230,'深60',12),label(X+300,1400,'長211.4',12),label(1100,2700,'入口延伸區'),label(bx+b['width']/2,2700,'床尾約115 cm'),
        f'<text x="{ox+W*s+25}" y="{oy+D*s/2}" font-size="14">320 cm</text>',
        '<text x="50" y="665" font-size="15">頂天櫃圖高 248.5 cm → 天花板暫採同高；包管下緣 208.5 cm</text>',
        '<text x="50" y="699" font-size="13">315含櫃深已確認。走道原述約80；暫採180寬床靠窗，櫃前剩75 cm。</text>',
        '<text x="50" y="728" font-size="13">按輸入尺寸建立的L1配置模型 · 非現場測繪／施工圖</text></g></svg>']
    (OUT/'preview.svg').write_text('\n'.join(svg))

def main():
    build();r=P['room'];b=P['bed'];c=P['wardrobe']
    checks=dict(part_count=len(PARTS),foot_clearance_mm=r['depth']-b['total_depth'],boxing_bottom_mm=r['height']-P['boxing']['drop'],wardrobe_to_bed_mm=r['head_wall']-c['depth']-b['width']-b['right_gap'],bed_to_window_wall_mm=b['right_gap'],maturity='L1',dimension_definition_pending=False,bed_dimensions_pending=True)
    assert checks['foot_clearance_mm']==1150
    assert checks['boxing_bottom_mm']==2085
    assert checks['wardrobe_to_bed_mm']>=0
    export_glb();plan()
    data=dict(parameters=P,parts=PARTS,colors=COLORS,checks=checks)
    (OUT/'geometry_mm.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    template=(ROOT/'scripts/room_a_viewer.html').read_text()
    (OUT/'index.html').write_text(template.replace('__DATA__',json.dumps(data,ensure_ascii=False)))
    (OUT/'model_checks.json').write_text(json.dumps(checks,indent=2))
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
