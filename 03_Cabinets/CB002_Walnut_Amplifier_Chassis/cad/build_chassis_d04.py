"""D04 concept. Run with FreeCAD Python; master dimensions here, mm."""
import FreeCAD as A, Part, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output'/'D04'; OUT.mkdir(exist_ok=True)
W,D,H,T=520.,380.,90.,20.
PW,PH,PT,R=444.,64.,6.,8.
TOP=4.
V=A.Vector
doc=A.newDocument('CB002_D04')
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
 o.addProperty('App::PropertyString','Evidence');o.Evidence='ASSUMED — D04 CONCEPT NOT FOR MANUFACTURE'
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
# D04: no central equipment window
for x,z in holes:front=front.cut(cyl(1.7,T+2,x,-1,z,(0,1,0)))
# Dowel pilot sockets crossing butt joints, along Y
for x in [10,W-10]:
 for z in [20,H-20]:front=front.cut(cyl(3.1,15,x,T-15,z,(0,1,0)))
add('W01_Front_Walnut',front,wood,(0,-40,0),'Walnut / grain X')
add('W02_Rear_Walnut',rear(front),wood,(0,40,0),'Walnut / grain X')
top_pts=[(37,y) for y in [70,D/2,D-70]]+[(W-37,y) for y in [70,D/2,D-70]]
for i,x in enumerate([0,W-T]):
 side=box(T,D-2*T,H,x,T,0)
 for y in [T,D-T-15]:
  for z in [20,H-20]:side=side.cut(cyl(3.1,15,x+10,y,z,(0,1,0)))
 for yy in [70,D/2,D-70]:
  for dy in [-6,6]:
   side=side.cut(cyl(3,10,10 if i==0 else W-20,yy+dy,72,(1,0,0)))
 add('W0%d_Side_Walnut'%(i+3),side,wood,((-35 if i==0 else 35),0,0),'Walnut / grain Y')
plate=rr(panel_x,panel_z,PW,PH,R,0,PT)
for x,z in holes:plate=plate.cut(cyl(1.25,4,x,PT,z,(0,-1,0)))
add('A01_Front_Blank',plate,gold,(0,-95,0),'Aluminium / gold finish provisional')
add('A02_Rear_Blank',rear(plate),gold,(0,95,0),'Aluminium / gold finish provisional')
# Monolithic stepped plate: perimeter 4 thick, central area 8 thick.
top=box(W,D,4,0,0,H).fuse(box(W-41,D-41,4,20.5,20.5,H-4)).removeSplitter()
for x,y in top_pts:top=top.cut(cyl(1.65,6,x,y,H-4))
add('A03_Stepped_Hidden_Top',top,gold,(0,0,110),'Aluminium / 8 blank, perimeter 4')
for back in [False,True]:
 for j,y in enumerate([70,D/2,D-70]):
  prefix=('RB' if back else 'LB')+str(j)
  conv=rear if back else lambda s:s
  offset=(35 if back else -35,0,25)
  bracket=box(3,24,22,20,y-12,64).fuse(box(28,24,3,20,y-12,83)).removeSplitter()
  cut=cyl(2.25,5,35.5,y,82).fuse(cyl(2.25,5,38.5,y,82)).fuse(box(3,4.5,5,35.5,y-2.25,82))
  bracket=bracket.cut(cut)
  for dy in [-6,6]:bracket=bracket.cut(cyl(2.25,5,19,y+dy,72,(1,0,0)))
  add(prefix+'_Bracket',conv(bracket),steel,offset,'Aluminium angle, 3 thick provisional')
  washer=cyl(4.5,1,37,y,82).cut(cyl(2.25,1,37,y,82))
  screw=cyl(2,8,37,y,82).fuse(cyl(3.5,3,37,y,79))
  screw=screw.cut(box(4,1,1.1,35,y-.5,78.9))
  add(prefix+'_TopWasher',conv(washer),steel,(0,0,-20))
  add(prefix+'_Up_M4x8',conv(screw),steel,(0,0,-35))
  for k,dy in enumerate([-6,6]):
   ins=cyl(3,10,10,y+dy,72,(1,0,0)).cut(cyl(1.65,10,10,y+dy,72,(1,0,0)))
   washer=cyl(4.5,1,23,y+dy,72,(1,0,0)).cut(cyl(2.25,1,23,y+dy,72,(1,0,0)))
   screw=cyl(2,12,12,y+dy,72,(1,0,0)).fuse(cyl(3.5,3,24,y+dy,72,(1,0,0)))
   screw=screw.cut(box(1.1,4,1,26,y+dy-2,71.5))
   add(prefix+'_Insert'+str(k),conv(ins),gold,offset,'M4 wood insert OD6x10 placeholder')
   add(prefix+'_SideWasher'+str(k),conv(washer),steel,offset)
   add(prefix+'_Side_M4x12_'+str(k),conv(screw),steel,offset)
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
doc.recompute();doc.saveAs(str(OUT/'CB002_D04.FCStd'))
Part.export(shapes,str(OUT/'CB002_D04_assembly.step'))
for o in shapes[:7]:Part.export([o],str(OUT/(o.Name+'.step')))
(OUT/'mesh_scene.json').write_text(json.dumps(parts))
# Non-fastener structure must not intersect; all threaded contact simplified.
struct=shapes[:7]+[o for o in shapes if o.Name.endswith('_Bracket')]
for i,a in enumerate(struct):
 for b in struct[i+1:]:assert a.Shape.common(b.Shape).Volume<.01,(a.Name,b.Name)
for o in shapes:
 if o.Name.startswith(('F_','R_')) or '_Side_M4' in o.Name or '_Up_M4' in o.Name or 'Washer' in o.Name:
  for w in shapes[:4]:assert o.Shape.common(w.Shape).Volume<.01,(o.Name,w.Name)
# Straight 8mm-diameter screwdriver approach from open bottom to each vertical head.
for x,y in top_pts:
 tool=cyl(4,78.9,x,y,0)
 for o in struct:assert tool.common(o.Shape).Volume<.01,('Tool approach',o.Name,x,y)
# Top face has no holes; exact volume of the highest 0.5mm slab must be W*D*.5.
assert abs(top.common(box(W,D,.5,0,0,93.5)).Volume-W*D*.5)<.01
roundtrip=Part.read(str(OUT/'CB002_D04_assembly.step'))
assert len(roundtrip.Solids)==len(shapes) and roundtrip.isValid()
report=['D04 concept validation',str(len(shapes))+' valid positive-volume solids; STEP readback valid.',
'Wood, plates and six brackets: zero volumetric interference.',
'All wood/fastener clearance checks pass; no front/rear central windows or screw-head counterbores.',
'Top highest 0.5mm full slab verified: no top-surface holes.',
'Six vertical Ø8 tool approach cylinders from bottom clear wood/plates/brackets. Tool/hand usability still requires physical trial.',
'Top M4x8: washer1 + bracket3 + thread engagement4; drill-bottom margin2.',
'Side M4x12: washer1 + bracket3 + insert engagement8.',
'Front/rear M3x18: washer1 + wood14 + engagement3.',
'No structural, thermal, electrical or manufacturing release; threads are envelopes.']
(OUT/'validation.txt').write_text('\n'.join(report))
(OUT/'BOM.csv').write_text('Part,Quantity,Description,Status\nW01-W02,2,Walnut 520x20x90 with outer rebate - NO centre window,ASSUMED\nW03-W04,2,Walnut 20x340x90 with side insert seats,ASSUMED\nA01-A02,2,Aluminium 444x64x6 R8 blind fixing holes,ASSUMED\nA03,1,Stepped top 520x380 perimeter4 centre8 no visible holes,ASSUMED\nL bracket,6,3mm aluminium concept,ASSUMED\nM3x18,12,Front rear panel screws,ASSUMED\nM3 washer,12,1mm thick,ASSUMED\nM4x8,6,Upward top screws,ASSUMED\nM4x12,12,Side bracket screws,ASSUMED\nM4 washer,18,1mm thick,ASSUMED\nM4 wood insert,12,OD6x10 supplier TBD,ASSUMED\nWood dowel,8,Diameter6 length30 fit TBD,ASSUMED\n')
for o in shapes:
 if o.Name.endswith('_Bracket'):Part.export([o],str(OUT/(o.Name+'.step')))
print('\n'.join(report))
