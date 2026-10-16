"""D01 concept. Run with FreeCAD Python; master dimensions here, mm."""
import FreeCAD as A, Part, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
W,D,H,T=520.,380.,90.,20.
PW,PH,PT,R=444.,64.,6.,8.
TOP=4.
V=A.Vector
doc=A.newDocument('CB002_D01')
parts=[]; shapes=[]
wood=(0.24,0.105,0.045); gold=(0.72,0.51,0.22); steel=(0.33,0.36,0.4)
def box(w,d,h,x,y,z): return Part.makeBox(w,d,h,V(x,y,z))
def cyl(r,l,x,y,z,axis=(0,0,1)):return Part.makeCylinder(r,l,V(x,y,z),V(*axis))
def rr(x,z,w,h,r,y,depth):
 s=box(w-2*r,depth,h,x+r,y,z).fuse(box(w,depth,h-2*r,x,y,z+r))
 for xx in [x+r,x+w-r]:
  for zz in [z+r,z+h-r]:s=s.fuse(cyl(r,depth,xx,y,zz,(0,1,0)))
 return s.removeSplitter()
def rear(s):
 s=s.copy();s.rotate(V(W/2,D/2,0),V(0,0,1),180);return s

def add(name,s,color,offset=(0,0,0),material=''):
 assert s.isValid() and s.Volume>0,name
 o=doc.addObject('PartDesign::Feature',name);o.Label=name;o.Shape=s
 o.addProperty('App::PropertyString','Evidence');o.Evidence='ASSUMED — D01 CONCEPT NOT FOR MANUFACTURE'
 o.addProperty('App::PropertyString','Material');o.Material=material
 o.addProperty('App::PropertyVector','ExplodedOffset');o.ExplodedOffset=V(*offset)
 if A.GuiUp:o.ViewObject.ShapeColor=color
 verts,tris=s.tessellate(0.18)
 parts.append(dict(name=name,color=color,offset=offset,vertices=[[v.x,v.y,v.z] for v in verts],faces=tris,volume=s.Volume))
 shapes.append(o);return o
panel_x=(W-PW)/2;panel_z=(H-PH)/2
holes=[(W/2-214,H/2),(W/2+214,H/2)]+[(x,H/2+z) for x in [W/2-140,W/2+140] for z in [-26,26]]
front=box(W,T,H,0,0,0)
front=front.cut(rr(panel_x-.3,panel_z-.3,PW+.6,PH+.6,R+.3,-.1,6.1))
front=front.cut(rr(W/2-202,H/2-20,404,40,6,-1,T+2))
for x,z in holes:front=front.cut(cyl(1.7,T+2,x,-1,z,(0,1,0)))
# Dowel pilot sockets crossing butt joints, along Y
for x in [10,W-10]:
 for z in [20,H-20]:front=front.cut(cyl(3.1,15,x,T-15,z,(0,1,0)))
add('W01_Front_Walnut',front,wood,(0,-40,0),'Walnut / grain X')
add('W02_Rear_Walnut',rear(front),wood,(0,40,0),'Walnut / grain X')
top_pts=[(10,y) for y in [50,D/2,D-50]]+[(W-10,y) for y in [50,D/2,D-50]]
for i,x in enumerate([0,W-T]):
 side=box(T,D-2*T,H,x,T,0)
 for y in [T,D-T-15]:
  for z in [20,H-20]:side=side.cut(cyl(3.1,15,x+10,y,z,(0,1,0)))
 for xx,yy in top_pts:
  if x<=xx<=x+T:side=side.cut(cyl(3,10,xx,yy,H-10))
 add('W0%d_Side_Walnut'%(i+3),side,wood,((-35 if i==0 else 35),0,0),'Walnut / grain Y')
plate=rr(panel_x,panel_z,PW,PH,R,0,PT)
for x,z in holes:plate=plate.cut(cyl(1.25,4,x,PT,z,(0,-1,0)))
add('A01_Front_Blank',plate,gold,(0,-95,0),'Aluminium / gold finish provisional')
add('A02_Rear_Blank',rear(plate),gold,(0,95,0),'Aluminium / gold finish provisional')
top=box(W,D,TOP,0,0,H)
for i,(x,y) in enumerate(top_pts):
 if i==0:cut=cyl(2.25,TOP+2,x,y,H-1)
 else:cut=cyl(2.25,TOP+2,x-1.5,y,H-1).fuse(cyl(2.25,TOP+2,x+1.5,y,H-1)).fuse(box(3,4.5,TOP+2,x-1.5,y-2.25,H-1))
 top=top.cut(cut)
add('A03_Top_Blank',top,gold,(0,0,100),'Aluminium / 4 mm provisional')
for i,(x,y) in enumerate(top_pts):
 insert=cyl(3,10,x,y,H-10).cut(cyl(1.65,10,x,y,H-10))
 add('I%02d_M4_Insert_Envelope'%i,insert,(.5,.38,.15),(0,0,30),'Supplier-dependent envelope, no threads')
 washer=cyl(4.5,1,x,y,H+TOP).cut(cyl(2.25,1,x,y,H+TOP))
 add('TW%02d_M4_Washer'%i,washer,steel,(0,0,115))
 screw=cyl(2,12,x,y,H+TOP+1-12).fuse(cyl(3.5,3,x,y,H+TOP+1))
 screw=screw.cut(box(4,1,1.2,x-2,y-.5,H+TOP+3))
 add('TS%02d_M4x12_Screw'%i,screw,steel,(0,0,130),'Simplified screw, no threads')
for back in [False,True]:
 for i,(x,z) in enumerate(holes):
  washer=cyl(3.5,1,x,T,z,(0,1,0)).cut(cyl(1.7,1,x,T,z,(0,1,0)))
  screw=cyl(1.5,18,x,T+1-18,z,(0,1,0)).fuse(cyl(2.8,2,x,T+1,z,(0,1,0)))
  # shallow slot on interior-facing head
  screw=screw.cut(box(3.5,1.1,.8,x-1.75,T+2,z-.4))
  for suffix,ss in [('Washer',washer),('M3x18',screw)]:
   add(('R' if back else 'F')+'_%02d_'%i+suffix,rear(ss) if back else ss,steel,(0,65 if back else -65,0),'Simplified fastener')
for back in [False,True]:
 for i,(x,z) in enumerate([(x,z) for x in [10,W-10] for z in [20,H-20]]):
  dow=cyl(3,30,x,T-15,z,(0,1,0))
  add(('RD' if back else 'FD')+str(i),rear(dow) if back else dow,(.55,.35,.16),(0,25 if back else -25,0),'Wood dowel / provisional')
meta=doc.addObject('App::FeaturePython','Master_Dimensions')
for k,v in [('Width',W),('Depth',D),('WoodHeight',H),('WoodThickness',T),('TopThickness',TOP),('PanelWidth',PW),('PanelHeight',PH),('PanelThickness',PT)]:
 meta.addProperty('App::PropertyLength',k);setattr(meta,k,v)
meta.addProperty('App::PropertyString','Rebuild');meta.Rebuild='Edit constants in cad/build_chassis.py and rerun; metadata is not a live feature driver.'
doc.recompute();doc.saveAs(str(OUT/'CB002_D01.FCStd'))
Part.export(shapes,str(OUT/'CB002_D01_assembly.step'))
for o in shapes[:7]:Part.export([o],str(OUT/(o.Name+'.step')))
(OUT/'mesh_scene.json').write_text(json.dumps(parts))
# Check non-fastener structural overlaps. Clearance, dowel/insert bore offsets verified separately.
struct=shapes[:7]; report=['D01 GEOMETRY VALIDATION','All %d shapes valid, positive volume.'%len(shapes)]
for i,a in enumerate(struct):
 for b in struct[i+1:]:
  vol=a.Shape.common(b.Shape).Volume
  assert vol<.01,(a.Name,b.Name,vol)
report+=['Main seven parts: no volumetric interference.','Front/back symmetric via 180deg rotation.','Panel M3x18: washer under-head Y=21; tip Y=3; plate rear Y=6; engagement 3, nominal drill-bottom margin 1 mm. Threads not modeled.','Top M4x12: under-head Z=95; tip Z=83; insert Z=80..90; engagement 7 mm.','No structural/thermal/electrical validation. No machining tolerances released.']
(OUT/'validation.txt').write_text('\n'.join(report))
(OUT/'BOM.csv').write_text('Part,Quantity,Description,Status\nW01-W02,2,Walnut 520x20x90 with pockets,ASSUMED\nW03-W04,2,Walnut 20x340x90,ASSUMED\nA01-A02,2,Aluminium 444x64x6 R8 with blind fixing holes,ASSUMED\nA03,1,Aluminium 520x380x4 with fixing holes,ASSUMED\nM3x18,12,Panel screws - verify effective blind thread,ASSUMED\nM3 washer,12,1mm thick,ASSUMED\nM4x12,6,Top screws,ASSUMED\nM4 washer,6,1mm thick,ASSUMED\nM4 wood insert,6,OD6x10 envelope supplier TBD,ASSUMED\nWood dowel,8,Diameter6 length30 fit TBD,ASSUMED\n')
print('\n'.join(report))
