#!/usr/bin/env python3
"""Deterministic six-camera CAD rasterization. Requires NumPy and Pillow.
No AI imagery is used to derive geometry. Triangle depth-buffer, actual mesh.
"""
import base64
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'02_Tables/TB001_D16_Three_Tier/models/D06'
G=OUT/'gallery';G.mkdir(exist_ok=True)
DATA=json.loads((OUT/'geometry_mm.json').read_text());VIEWS=json.loads((OUT/'views.json').read_text())
COLORS={'SMOKED_OAK':'594638','NATURAL_OAK':'c8aa7d'}
def normalize(v):return v/np.linalg.norm(v)

def render(spec):
    width,height=900,1000;aspect=width/height
    toward=normalize(np.array(spec['position'])-spec['target'])
    right=normalize(np.cross(spec['up'],toward));up=np.cross(toward,right)
    matrix=np.array([right,up,toward]).T;target=np.array(spec['target'])
    span=spec['span']*max(1,1/aspect);scale=height/span
    buffer=np.full((height,width),-np.inf);canvas=np.full((height,width,3),[244,240,232],dtype=np.uint8)
    light=normalize(np.array([-1.0,-1.5,2.5]))
    for part in DATA['parts']:
        world=np.array(part['vertices_mm'])/1000
        coords=(world-target)@matrix
        coords[:,0]=coords[:,0]*scale+width/2;coords[:,1]=-coords[:,1]*scale+height/2
        rgb=np.array([int(COLORS[part['material']][i:i+2],16) for i in (0,2,4)])
        for face in part['faces']:
            n=normalize(np.cross(world[face[1]]-world[face[0]],world[face[2]]-world[face[0]]))
            if np.dot(n,toward)<=1e-8:continue
            shade=np.clip(rgb*(.69+.34*max(0,np.dot(n,light))),0,255).astype(np.uint8)
            for j in range(1,len(face)-1):
                tri=coords[[face[0],face[j],face[j+1]]];a,b,c=tri
                xmin=max(0,int(np.floor(tri[:,0].min())));xmax=min(width-1,int(np.ceil(tri[:,0].max())))
                ymin=max(0,int(np.floor(tri[:,1].min())));ymax=min(height-1,int(np.ceil(tri[:,1].max())))
                if xmin>xmax or ymin>ymax:continue
                xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
                den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
                if abs(den)<1e-10:continue
                u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
                v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den
                w=1-u-v;z=u*a[2]+v*b[2]+w*c[2]
                patch=buffer[ymin:ymax+1,xmin:xmax+1]
                mask=(u>=-1e-8)&(v>=-1e-8)&(w>=-1e-8)&(z>patch)
                patch[mask]=z[mask];canvas[ymin:ymax+1,xmin:xmax+1][mask]=shade
    return Image.fromarray(canvas)

def main():
    manifest={'geometry_sha256':hashlib.sha256((OUT/'geometry_mm.json').read_bytes()).hexdigest(),'renderer':'triangle z-buffer / NumPy + Pillow','views':{}}
    fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
    font=ImageFont.truetype(fontpath,25);small=ImageFont.truetype(fontpath,18)
    sheet=Image.new('RGB',(1800,1420),'#f4f0e8');draw=ImageDraw.Draw(sheet)
    draw.text((35,24),'TB001 / D06  —  QUIET FRAME / FINE LINES',font=font,fill='#382e25')
    draw.text((35,60),'D05 unchanged + 2 fine side lines | W600 x D480 x H600 mm | L1 — NOT FOR PRODUCTION',font=small,fill='#776754')
    for i,(name,spec) in enumerate(VIEWS.items()):
        im=render(spec);path=G/f'{name}_cad.png';im.save(path)
        manifest['views'][name]={'camera':spec,'cad':path.name,'cad_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        thumb=im.resize((540,600),Image.Resampling.LANCZOS);x=30+(i%3)*590;y=110+(i//3)*650
        sheet.paste(thumb,(x,y));draw.text((x,y+602),name.upper()+' / CAD',font=small,fill='#382e25')
    sheet.save(OUT/'preview.svg.png')
    encoded=base64.b64encode((OUT/'preview.svg.png').read_bytes()).decode()
    (OUT/'preview.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1420" viewBox="0 0 1800 1420"><title>D06 six actual-mesh CAD views; not production drawings</title><image width="1800" height="1420" href="data:image/png;base64,{encoded}"/></svg>')
    (G/'cad_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print('Six CAD cameras + uncropped overview rendered.')
if __name__=='__main__':main()
