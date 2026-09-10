#!/usr/bin/env python3
"""D16-inspired TB001 D01. Dependency-free, mm source / metre GLB.

Generates exterior design geometry, not joinery or a production cut list.
Run from any directory: python3 scripts/tb001_three_tier.py
"""
import csv
import itertools
import json
import math
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '02_Tables/TB001_D16_Three_Tier/models/D01'
P = json.loads((OUT / 'parameters.json').read_text())
PARTS = []
COLORS = {'WALNUT': '#63432e', 'MAPLE': '#d9bd89'}
FACES = [[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]


def box(name, group, material, x, y, z, w, d, h):
    assert min(w, d, h) > 0, name
    vertices = [[x,y,z],[x+w,y,z],[x+w,y+d,z],[x,y+d,z],
                [x,y,z+h],[x+w,y,z+h],[x+w,y+d,z+h],[x,y+d,z+h]]
    PARTS.append(dict(id=f'P{len(PARTS)+1:03}', name=name, group=group,
                      material=material, origin_mm=[x,y,z], size_mm=[w,d,h],
                      vertices_mm=vertices, faces=FACES))


def build():
    w,d,h = P['width'],P['depth'],P['height']
    sx,sy,s = P['post_x'],P['post_y'],P['setback']
    e,foot,tt = P['leg_edge'],P['foot_height'],P['top_thickness']
    # Nonoverlapping 3x3 cross-section: maple body and dark corner strips.
    for i,x in enumerate([s,w-s-sx]):
        for j,y in enumerate([s,d-s-sy]):
            name=f'Leg {i+1}{j+1}'
            box(name+' foot','Legs','WALNUT',x,y,0,sx,sy,foot)
            xx=[(0,e),(e,sx-2*e),(sx-e,e)]
            yy=[(0,e),(e,sy-2*e),(sy-e,e)]
            for a,(dx,ww) in enumerate(xx):
                for b,(dy,dd) in enumerate(yy):
                    mat='WALNUT' if a!=1 and b!=1 else 'MAPLE'
                    box(f'{name} segment {a}{b}','Legs',mat,x+dx,y+dy,foot,ww,dd,h-tt-foot)
    for label,level in zip(['Lower','Middle'],P['surface_levels'][:2]):
        t=P['shelf_frame_thickness']; st=P['shelf_thickness']; g=P['panel_gap']
        for y in [s,d-s-sy]:
            box(label+' front/back rail',label,'WALNUT',s+sx,y,level-t,w-2*(s+sx),sy,t)
        for x in [s,w-s-sx]:
            box(label+' side rail',label,'WALNUT',x,s+sy,level-t,sx,d-2*(s+sy),t)
        box(label+' maple panel',label,'MAPLE',s+sx+g,s+sy+g,level-st,
            w-2*(s+sx+g),d-2*(s+sy+g),st)
    # Top aprons terminate between the posts and meet the top underside.
    a,at=P['apron_height'],P['apron_thickness']
    for y in [s,d-s-at]:
        box('Top front/back apron','Top','WALNUT',s+sx,y,h-tt-a,w-2*(s+sx),at,a)
    for x in [s,w-s-at]:
        box('Top side apron','Top','WALNUT',x,s+sy,h-tt-a,at,d-2*(s+sy),a)
    b,c,g=P['top_border'],P['top_centre_strip'],P['panel_gap']
    for y in [0,d-b]:
        box('Top front/back border','Top','WALNUT',0,y,h-tt,w,b,tt)
    for x in [0,w-b]:
        box('Top side border','Top','WALNUT',x,b,h-tt,b,d-2*b,tt)
    box('Top centre strip','Top','WALNUT',(w-c)/2,b,h-tt,c,d-2*b,tt)
    for x in [b+g,(w+c)/2+g]:
        box('Top maple panel','Top','MAPLE',x,b+g,h-tt,(w-c)/2-b-2*g,d-2*(b+g),tt)


def verify():
    vertices=[v for part in PARTS for v in part['vertices_mm']]
    bounds=[[min(v[k] for v in vertices),max(v[k] for v in vertices)] for k in range(3)]
    assert bounds == [[0,P['width']],[0,P['depth']],[0,P['height']]],bounds
    collisions=[]
    for a,b in itertools.combinations(PARTS,2):
        overlap=[min(a['origin_mm'][k]+a['size_mm'][k],b['origin_mm'][k]+b['size_mm'][k])-
                 max(a['origin_mm'][k],b['origin_mm'][k]) for k in range(3)]
        if min(overlap)>1e-8: collisions.append([a['id'],b['id']])
    assert not collisions,collisions
    for part in PARTS:
        edges={}
        for face in part['faces']:
            for a,b in zip(face,face[1:]+face[:1]):
                edges.setdefault(tuple(sorted([a,b])),[]).append((a,b))
        assert all(len(v)==2 and v[0]==v[1][::-1] for v in edges.values())
    return dict(bounds_mm=bounds,part_count=len(PARTS),positive_volume_overlap=collisions,
                closed_consistently_wound_meshes=True,
                surface_heights_mm=P['surface_levels'],
                clear_opening_front_mm=[P['surface_levels'][1]-P['shelf_frame_thickness']-P['surface_levels'][0],
                    P['height']-P['top_thickness']-P['apron_height']-P['surface_levels'][1]],
                maturity='L1',engineering_verified=False,
                note='Visual segments are not purchasing or cut-list quantities. Joinery and shelf retention unmodelled.')


def glb():
    binary=bytearray(); views=[]; accessors=[]; meshes=[]; nodes=[]
    for part in PARTS:
        positions=[]; normals=[]
        # glTF Y up: X,Y,Z mm -> X,Z,-Y m.
        vv=[[v[0]/1000,v[2]/1000,-v[1]/1000] for v in part['vertices_mm']]
        for f in part['faces']:
            u=[vv[f[1]][k]-vv[f[0]][k] for k in range(3)]
            v=[vv[f[2]][k]-vv[f[0]][k] for k in range(3)]
            n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
            length=math.sqrt(sum(x*x for x in n));n=[x/length for x in n]
            for tri in [(f[0],f[1],f[2]),(f[0],f[2],f[3])]:
                for i in tri:positions.extend(vv[i]);normals.extend(n)
        attrs={}
        for kind,values in [('POSITION',positions),('NORMAL',normals)]:
            offset=len(binary);binary.extend(struct.pack('<'+'f'*len(values),*values))
            views.append(dict(buffer=0,byteOffset=offset,byteLength=len(values)*4,target=34962))
            acc=dict(bufferView=len(views)-1,componentType=5126,count=len(values)//3,type='VEC3')
            if kind=='POSITION':acc.update(min=[min(values[k::3]) for k in range(3)],max=[max(values[k::3]) for k in range(3)])
            accessors.append(acc);attrs[kind]=len(accessors)-1
        meshes.append(dict(name=part['id']+' '+part['name'],primitives=[dict(attributes=attrs,material=list(COLORS).index(part['material']))]))
        nodes.append(dict(mesh=len(meshes)-1,name=part['id']+' '+part['name']))
    materials=[dict(name=n,pbrMetallicRoughness=dict(baseColorFactor=[int(c[i:i+2],16)/255 for i in (1,3,5)]+[1],metallicFactor=0,roughnessFactor=.55)) for n,c in COLORS.items()]
    data=dict(asset=dict(version='2.0',generator='TB001 D01'),scene=0,scenes=[dict(nodes=list(range(len(nodes))))],nodes=nodes,meshes=meshes,materials=materials,buffers=[dict(byteLength=len(binary))],bufferViews=views,accessors=accessors)
    js=json.dumps(data,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
    out=struct.pack('<III',0x46546c67,2,28+len(js)+len(binary))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary
    (OUT/'TB001_D01.glb').write_bytes(out)
    # Read back container and accessors rather than trusting export alone.
    blob=(OUT/'TB001_D01.glb').read_bytes();assert struct.unpack_from('<I',blob,8)[0]==len(blob)
    size=struct.unpack_from('<I',blob,12)[0];parsed=json.loads(blob[20:20+size])
    assert len(parsed['meshes'])==len(PARTS)
    for view in parsed['bufferViews']:assert view['byteOffset']+view['byteLength']<=len(binary)


def svg():
    def project(v,mode):
        x,y,z=v
        if mode=='front':return x,-z,-y
        if mode=='side':return y,-z,-x
        if mode=='top':return x,y,z
        return .80*x-.60*y,.34*x+.453*y-.824*z,.494*x+.659*y+.566*z
    panels=[('persp',52,148,590,615,'01 / 三層 · D16 的雙色框架'),
            ('front',725,156,410,310,'02 / 正面'),('side',1160,156,345,310,'03 / 側面'),
            ('top',766,536,350,295,'04 / 俯視')]
    content=['<svg xmlns="http://www.w3.org/2000/svg" width="1560" height="1000" viewBox="0 0 1560 1000">',
        '<rect width="1560" height="1000" fill="#f4f0e8"/>',
        '<g font-family="Arial, PingFang TC, sans-serif" fill="#372c23">',
        '<text x="52" y="54" font-size="13" letter-spacing="4">TB001 / D01 · DESIGN STUDY</text>',
        '<text x="52" y="102" font-size="34">D16 三層邊几</text>',
        '<text x="725" y="94" font-size="23">W 600 × D 480 × H 600 mm</text>']
    for mode,x,y,w,h,label in panels:
        allp=[project(v,mode) for part in PARTS for v in part['vertices_mm']]
        minx,maxx=min(v[0] for v in allp),max(v[0] for v in allp)
        miny,maxy=min(v[1] for v in allp),max(v[1] for v in allp)
        scale=min(w/(maxx-minx),h/(maxy-miny))
        ox=x+(w-(maxx-minx)*scale)/2;oy=y+(h-(maxy-miny)*scale)/2
        polygons=[]
        for part in PARTS:
            for fi,face in enumerate(part['faces']):
                vertices=[part['vertices_mm'][i] for i in face]
                pp=[project(v,mode) for v in vertices]
                area=sum(pp[i][0]*pp[(i+1)%4][1]-pp[(i+1)%4][0]*pp[i][1] for i in range(4))
                # Screen-space winding: positive faces look toward this camera.
                # Front uses the opposite screen-handedness to other views.
                if (-area if mode=='front' else area)<=1e-6:continue
                color=COLORS[part['material']];factor=[.72,1.12,.94,.79,.86,.87][fi]
                shade='#'+''.join(f'{min(255,round(int(color[k:k+2],16)*factor)):02x}' for k in (1,3,5))
                # Split long surfaces so a leg does not sort as one face across
                # several shelf planes. Shared fill/stroke avoids tile seams.
                nu=max(1,math.ceil(math.dist(vertices[0],vertices[1])/12)) if mode=='persp' else 1
                nv=max(1,math.ceil(math.dist(vertices[0],vertices[3])/12)) if mode=='persp' else 1
                def point(u,v):
                    return project([vertices[0][k]+u*(vertices[1][k]-vertices[0][k])+v*(vertices[3][k]-vertices[0][k]) for k in range(3)],mode)
                for iu in range(nu):
                    for iv in range(nv):
                        qq=[point(i/nu,j/nv) for i,j in [(iu,iv),(iu+1,iv),(iu+1,iv+1),(iu,iv+1)]]
                        points=' '.join(f'{ox+(a-minx)*scale:.2f},{oy+(b-miny)*scale:.2f}' for a,b,_ in qq)
                        polygons.append((sum(p[2] for p in qq)/4,f'<polygon points="{points}" fill="{shade}" stroke="{shade}" stroke-width=".35"/>'))
        content.append(f'<text x="{x}" y="{y-17}" font-size="14">{label}</text>')
        content.extend(s for _,s in sorted(polygons,key=lambda a:a[0]))
        if mode in ['front','side']:
            xx=ox-18;top=oy;bottom=oy+600*scale
            content.append(f'<path d="M{xx+5},{top}h-10 M{xx},{top}V{bottom} M{xx+5},{bottom}h-10" fill="none" stroke="#8c7964"/>')
            content.append(f'<text x="{xx-7}" y="{(top+bottom)/2}" font-size="12" text-anchor="end">600</text>')
            content.append(f'<text x="{ox+w*0.35}" y="{bottom+24}" font-size="13">{600 if mode=="front" else 480} mm</text>')
        if mode=='front':
            for level in P['surface_levels']:
                yy=oy+(600-level)*scale
                content.append(f'<text x="{ox+600*scale+12}" y="{yy+4}" font-size="12">{level}</text>')
    content.extend(['<text x="1180" y="615" font-size="19">胡桃木框 × 楓木面</text>',
        '<text x="1180" y="654" font-size="15">桌面 + 中層 + 下層</text>',
        '<text x="1180" y="686" font-size="15">離地 600 / 350 / 140 mm</text>',
        '<text x="1180" y="718" font-size="15">30 × 40 mm 雙色細腳</text>',
        '<text x="1180" y="750" font-size="15">四面開放，頂面深色分隔條</text>',
        '<path d="M52 886H1508" stroke="#cdbfae"/>',
        '<text x="52" y="924" font-size="14">L1 外觀幾何方案 · 同一模型正交投影 · 單位 mm · 非生產圖／非開料尺寸</text>',
        '<text x="52" y="955" font-size="13" fill="#756655">寬深按使用者公分需求換算；高度、層位及截面為本輪設計。榫接、面板托持及實木活動量待工程化。</text>',
        '</g></svg>'])
    (OUT/'preview.svg').write_text('\n'.join(content))


def main():
    build();checks=verify()
    data=dict(revision='D01',units='mm',parameters=P,parts=PARTS)
    (OUT/'geometry_mm.json').write_text(json.dumps(data,separators=(',',':')))
    with (OUT/'parts_dimensions.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['id','name','group','material','x_mm','y_mm','z_mm','width_mm','depth_mm','height_mm','status'])
        for part in PARTS:writer.writerow([part['id'],part['name'],part['group'],part['material'],*part['origin_mm'],*part['size_mm'],'CONCEPT exterior, not cut list'])
    glb();svg()
    template=(ROOT/'scripts/tb001_viewer.html').read_text()
    (OUT/'TB001_D01_viewer.html').write_text(template.replace('__DATA__',json.dumps(data,separators=(',',':'))))
    (OUT/'model_checks.json').write_text(json.dumps(checks,indent=2))
    print(json.dumps(checks,indent=2))


if __name__=='__main__':main()
