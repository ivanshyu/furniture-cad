#!/usr/bin/env python3
"""Parameter-derived dimension sheet; outlines are CAD design projections, not CAM."""
import json,math,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=Path(os.environ.get('TB001_D07_OUT',str(R/'02_Tables/TB001_D16_Three_Tier/models/D07')));p=json.loads((O/'parameters.json').read_text())
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1100" viewBox="0 0 1400 1100"><rect width="1400" height="1100" fill="#faf7f1"/><style>text{font-family:Arial,sans-serif;fill:#382e25;font-size:17px}.title{font-size:28px}.dim{stroke:#82715e;stroke-width:1;fill:none}.maple{fill:#e5d6b5;stroke:#382e25;stroke-width:1.2}.walnut{fill:#63432e;stroke:#382e25;stroke-width:1}</style>']
def txt(x,y,t,c=''):svg.append(f'<text x="{x}" y="{y}" class="{c}">{t}</text>')
def rect(x,y,w,h,c):svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{c}"/>')
def dh(x1,x2,y,label):
 svg.append(f'<path class="dim" d="M{x1},{y-6}v12 M{x2},{y-6}v12 M{x1},{y}H{x2}"/>');txt((x1+x2)/2-40,y-10,label)
def dv(x,y1,y2,label):
 svg.append(f'<path class="dim" d="M{x-6},{y1}h12 M{x-6},{y2}h12 M{x},{y1}V{y2}"/>');txt(x+10,(y1+y2)/2,label)
txt(35,45,'TB001 / D07 — DIMENSION STUDY','title');txt(35,77,'2026-09-10 | mm | ASSUMED dimensions | L1 / NOT FOR PRODUCTION | separate views, not to printed scale')
# Upper plan at .65 scale.
sc=390/p['top_diameter'];cx=260;cy=335;rad=p['top_diameter']/2*sc
svg.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" class="maple"/>')
for L,W,r,c in [(p['grip_clear_length']+2*p['grip_trim'],p['grip_clear_width']+2*p['grip_trim'],p.get('grip_outer_corner_radius',p['grip_corner_radius']+p['grip_trim']),'walnut'),(p['grip_clear_length'],p['grip_clear_width'],p['grip_corner_radius'],'')]:
 svg.append(f'<rect x="{cx-L*sc/2}" y="{cy-W*sc/2}" width="{L*sc}" height="{W*sc}" rx="{r*sc}" class="{c}" fill="{ "#faf7f1" if not c else "#63432e"}"/>')
dh(cx-rad,cx+rad,125,f'Ø{p["top_diameter"]}');txt(70,565,'UPPER PLAN / solid maple / no circular edging')
# Leg projection in local tangential plane.
x=670;y=710;scale=.9;w=p['leg_width'];h=p['overall_height']-p['top_thickness'];b=p['crown_bearing_width'];shoe=p['shoe_height'];zc=h-math.sqrt((w/2)**2-(b/2)**2)
# Profile clockwise from bottom left through clipped semicircular crown.
x0=x-w/2*scale;x1=x+w/2*scale;yt=y-zc*scale;top=y-h*scale
svg.append(f'<path class="maple" d="M{x0},{y-shoe*scale}V{yt} A{w/2*scale},{w/2*scale} 0 0 1 {x-b/2*scale},{top} H{x+b/2*scale} A{w/2*scale},{w/2*scale} 0 0 1 {x1},{yt} V{y-shoe*scale}Z"/>')
s=p['shelf_top']-p['shelf_thickness'];cw=p['slot_clear_width'];tr=p['slot_trim']
rect(x-(cw/2+tr)*scale,y-(s+tr)*scale,(cw+2*tr)*scale,(s+tr-shoe)*scale,'walnut')
svg.append(f'<rect x="{x-cw/2*scale}" y="{y-s*scale}" width="{cw*scale}" height="{(s-shoe)*scale}" fill="#faf7f1"/>')
rect(x0,y-shoe*scale,w*scale,shoe*scale,'walnut')
for z in [s-p['x_height'],s-3*p['x_height'],s-5*p['x_height']]:rect(x-p['x_width']/2*scale,y-(z+p['x_height'])*scale,p['x_width']*scale,p['x_height']*scale,'walnut')
for i in range(p.get('upper_band_count',0)):
 bandtop=zc-p['upper_band_crown_clearance']-i*(p['upper_band_height']+p['upper_band_gap'])
 rect(x0,y-bandtop*scale,w*scale,p['upper_band_height']*scale,'walnut')
dh(x0,x1,745,str(w));dv(760,top,y,f'{h}');txt(560,785,'LOCAL LEG / thickness 20');txt(560,812,'Crown R60 / bearing flat 30');txt(560,839,'Slot clear 24 / trim 4 / shoe H18')
# Section elevation of table levels, schematic edge-on X bars.
x=1030;z0=710;sc=.85;rr=p['top_diameter']/2
rect(x-rr*.55,z0-p['overall_height']*sc,rr*1.1,p['top_thickness']*sc,'maple')
rect(x-p['shelf_diameter']*.55/2,z0-p['shelf_top']*sc,p['shelf_diameter']*.55,p['shelf_thickness']*sc,'maple')
for z in [s-p['x_height'],s-3*p['x_height'],s-5*p['x_height']]:rect(x-132,z0-(z+p['x_height'])*sc,264,p['x_height']*sc,'walnut')
dv(1230,z0-p['overall_height']*sc,z0,str(p['overall_height']));txt(920,760,'LEVELS / horizontal width schematic');txt(920,790,f'Upper underside {p["overall_height"]-p["top_thickness"]} / shelf top {p["shelf_top"]}');txt(920,818,f'X tops: {s} / {s-2*p["x_height"]} / {s-4*p["x_height"]}');txt(920,846,'X height 14 / clear gap 14 / stack 70')
# Grip enlargement.
L=p['grip_clear_length'];W=p['grip_clear_width'];tr=p['grip_trim'];r=p['grip_corner_radius'];k=2.5;gx=255;gy=725
svg.append(f'<rect x="{gx-(L/2+tr)*k}" y="{gy-(W/2+tr)*k}" width="{(L+2*tr)*k}" height="{(W+2*tr)*k}" rx="{p.get('grip_outer_corner_radius',r+tr)*k}" class="walnut"/>')
svg.append(f'<rect x="{gx-L*k/2}" y="{gy-W*k/2}" width="{L*k}" height="{W*k}" rx="{r*k}" fill="#faf7f1"/>')
dh(gx-L*k/2,gx+L*k/2,650,f'{L} clear');dv(415,gy-W*k/2,gy+W*k/2,str(W));txt(60,830,f'GRIP / inner R{r} / four solid walnut strips');txt(60,860,f'Net {L} × {W} / outer {L+2*tr} × {W+2*tr} / through {p["top_thickness"]}')
txt(40,910,f'Grip trim {tr} = X bar height {p["x_height"]} / shelf diameter {p["shelf_diameter"]} / clear height {p["overall_height"]-p["top_thickness"]-p["shelf_top"]}');txt(40,945,'Design relations confirmed; numeric sizing is provisional. Grip requires a full-size hand-fit trial.')
txt(40,980,'Top/shelf retention, foot joints, wood movement, pin sizing and load testing remain unresolved.')
txt(40,1015,'Native BRep: TB001_D07.FCStd / STEP. No veneer; lower shelf unperforated. Not a rated carrying handle.')
svg.append('</svg>');(O/'dimensions.svg').write_text('\n'.join(svg)+'\n')
