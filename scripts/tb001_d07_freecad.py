#!/usr/bin/env python3
"""D07 BRep concept CAD. Run with FreeCAD bundled Python; JSON is master.
No AI geometry. Not a production drawing or a load-rated carrying handle.
"""
import sys, json, math, csv
from pathlib import Path
import os
sys.path.insert(0, '/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App, Part, Import
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('TB001_D07_OUT',str(ROOT/'02_Tables/TB001_D16_Three_Tier/models/D07')))
OUT.mkdir(parents=True,exist_ok=True)
DEFAULT={
 'revision':'D07','units':'mm','maturity':'L1 / engineering draft — NOT FOR PRODUCTION',
 'dimension_status':'ASSUMED unless explicitly identified as user-required relation',
 'top_diameter':600,'overall_height':600,'top_thickness':20,
 'shelf_diameter':420,'shelf_top':320,'shelf_thickness':20,
 'leg_radius':225,'leg_width':120,'leg_thickness':20,'crown_bearing_width':30,
 'shoe_height':18,'shoe_depth':24,'slot_clear_width':24,'slot_trim':4,
 'grip_clear_length':95,'grip_clear_width':30,'grip_corner_radius':3,'grip_trim':4,
 'x_height':14,'x_width':18,'x_projection':8,'cross_pin_diameter':6,
 'requirements':['Four arched maple blade legs','Open-bottom rectangular leg slots with walnut shoes',
 'Three horizontal walnut X frames; clear gap equals bar height','Two solid maple circular surfaces; no walnut circular edging or veneer',
 'Small walnut-framed grip ONLY in upper surface; lower surface unperforated'],
 'unverified':['95 × 30 grip requires physical four-finger trial','All dimensions and structural sizing',
 'Tabletop and shelf retention, wood movement, foot joinery, pin fit and load capacity']}
PARAM=OUT/'parameters.json'
if not PARAM.exists(): PARAM.write_text(json.dumps(DEFAULT,ensure_ascii=False,indent=2)+'\n')
p=json.loads(PARAM.read_text()); V=App.Vector
if p.get('grip_trim_matches')=='x_height':
 assert p['grip_trim']==p['x_height'], 'Grip trim must match X bar height'
assert p['overall_height']-p['top_thickness']>p['shelf_top']
parts=[]
def box(x,y,z,a,b,c): return Part.makeBox(a,b,c,V(x,y,z))
def add(name,material,role,shape,grain):
 shape=shape.removeSplitter()
 assert shape.isValid() and len(shape.Solids)==1 and shape.Volume>0,name
 parts.append(dict(id=f'P{len(parts)+1:02}',name=name,material=material,group=role,shape=shape,grain=grain))
 return parts[-1]
def radial(shape,angle):
 s=shape.copy();s.rotate(V(0,0,0),V(0,0,1),angle);return s

def rr(length,width,r,z,h):
 # Zero radius is an exact square-cornered rectangle.
 if r==0:return box(-length/2,-width/2,z,length,width,h)
 # Exact rounded rectangle, centred in XY; continuous tangency.
 s=box(-length/2+r,-width/2,z,length-2*r,width,h).fuse(box(-length/2,-width/2+r,z,length,width-2*r,h))
 for x in [-length/2+r,length/2-r]:
  for y in [-width/2+r,width/2-r]:s=s.fuse(Part.makeCylinder(r,h,V(x,y,z)))
 return s.removeSplitter()
def poly(points,z,h):
 wire=Part.makePolygon([V(x,y,z) for x,y in points]+[V(*points[0],z)])
 return Part.Face(wire).extrude(V(0,0,h))
H=p['overall_height'];tt=p['top_thickness'];zt=H-tt
s=p['shelf_top']-p['shelf_thickness'];h=p['x_height'];R=p['leg_radius'];w=p['leg_width'];t=p['leg_thickness'];shoe=p['shoe_height'];trim=p['slot_trim'];clear=p['slot_clear_width']
assert p['shelf_diameter']/2<R-t/2
assert p['x_width']<clear
assert p['crown_bearing_width']<w
L=p['grip_clear_length'];W=p['grip_clear_width'];q=p['grip_trim'];r=p['grip_corner_radius']
outer=rr(L+2*q,W+2*q,p.get('grip_outer_corner_radius',r+q),zt,tt)
inner=rr(L,W,r,zt,tt)
add('Upper circular maple top with grip recess','MAPLE','upper_top',Part.makeCylinder(p['top_diameter']/2,tt,V(0,0,zt)).cut(outer),'X; solid edge-glued maple')
ring=outer.cut(inner)
a=(L+2*q)/2;b=(W+2*q)/2;d=a-b
regions=[('north',[(-a,b),(a,b),(d,0),(-d,0)]),('south',[(-a,-b),(-d,0),(d,0),(a,-b)]),('east',[(a,-b),(d,0),(a,b)]),('west',[(-a,-b),(-a,b),(-d,0)])]
for name,pts in regions:add('Grip mitred strip '+name,'WALNUT','grip_trim',ring.common(poly(pts,zt,tt)),'Along strip; solid walnut')
add('Lower circular maple shelf — no opening','MAPLE','lower_top',Part.makeCylinder(p['shelf_diameter']/2,p['shelf_thickness'],V(0,0,s)),'X; solid edge-glued maple')
# Local blade: radial X, tangential Y, vertical Z. Semicircular crown
# clipped to a 30 mm bearing flat, rather than a tangent-only contact.
zc=zt-math.sqrt((w/2)**2-(p['crown_bearing_width']/2)**2)
blade=box(R-t/2,-w/2,shoe,t,w,zc-shoe).fuse(Part.makeCylinder(w/2,t,V(R-t/2,0,zc),V(1,0,0)))
blade=blade.common(box(R-t/2,-w/2,shoe,t,w,zt-shoe))
blade=blade.cut(box(R-t/2-1,-(clear+2*trim)/2,shoe,t+2,clear+2*trim,s+trim-shoe))
bands=[]
for i in range(p.get('upper_band_count',0)):
 bh=p['upper_band_height'];depth=p['upper_band_depth']
 assert 0<depth<=t and bh>0
 bandtop=zc-p['upper_band_crown_clearance']-i*(bh+p['upper_band_gap'])
 assert bandtop-bh>s+trim, 'Upper accent overlaps slot lintel'
 band=box(R+t/2-depth,-w/2,bandtop-bh,depth,w,bh)
 blade=blade.cut(band);bands.append(band)
angles=[45,135,225,315];zs=[s-h,s-3*h,s-5*h]
# Real cross-bored dowels transfer rail load into blade cheeks. Nominal fit;
# engineering verification of the pin and reduced rod section remains open.
pins=[]
for angle in angles:
 holes=[Part.makeCylinder(p['cross_pin_diameter']/2,w,V(R,-w/2,z+h/2),V(0,1,0)) for z in zs]
 def drilled(shape):
  for hole in holes:shape=shape.cut(hole)
  return radial(shape,angle)
 for segment,solid in enumerate(sorted(drilled(blade).Solids,key=lambda sh:sh.BoundBox.ZMin)):
  add(f'Arched blade {angle} / maple segment {segment+1}','MAPLE','leg',solid,'Vertical Z; segment joints TO VERIFY')
 for side in [-1,1]:
  y=clear/2 if side==1 else -clear/2-trim
  add(f'Slot jamb {angle} / {side}','WALNUT','slot_trim',drilled(box(R-t/2,y,shoe,t,trim,s-shoe)),'Vertical Z')
 add(f'Slot lintel {angle}','WALNUT','slot_trim',radial(box(R-t/2,-clear/2-trim,s,t,clear+2*trim,trim),angle),'Tangential')
 add(f'Foot shoe {angle}','WALNUT','foot',radial(box(R-p['shoe_depth']/2,-w/2,0,p['shoe_depth'],w,shoe),angle),'Tangential; shoe-to-leg joint unresolved')
 for k,hole in enumerate(holes):pins.append((f'Cross pin {angle} / level {k+1}',radial(hole,angle)))
length=2*(R+t/2+p['x_projection']);bw=p['x_width']
for level,z in enumerate(zs):
 for j,angle in enumerate([45,135]):
  beam=box(-length/2,-bw/2,z,length,bw,h)
  notch_z=z+h/2 if j==0 else z
  beam=beam.cut(box(-bw/2,-bw/2-1,notch_z,bw,bw+2,h/2))
  # Endpoint transverse pin axes are perpendicular to beam.
  for sign in [-1,1]:beam=beam.cut(Part.makeCylinder(p['cross_pin_diameter']/2,bw,V(sign*R,-bw/2,z+h/2),V(0,1,0)))
  add(f'X level {level+1} beam {j+1}','WALNUT','x_rail',radial(beam,angle),'Along beam; half-lap centre; drilled ends')
for angle in angles:
 for i,band in enumerate(bands):
  add(f'Upper transition band {angle} / {i+1}','WALNUT','upper_accent',radial(band,angle),'Tangential; full-thickness structural splice, joints NOT DESIGNED' if p.get('upper_band_through') else 'Tangential; solid inlay, cross-grain joint TO VERIFY')
for name,shape in pins:add(name,'WALNUT','cross_pin',shape,'Along pin; strength / fit TO VERIFY')
# Exact BRep validation. Contact is allowed, positive-volume interference is not.
collisions=[]
for i,a0 in enumerate(parts):
 for b0 in parts[i+1:]:
  aa=a0['shape'];bb=b0['shape']
  if aa.BoundBox.intersect(bb.BoundBox):
   v=aa.common(bb).Volume
   if v>0.001:collisions.append({'a':a0['id'],'b':b0['id'],'volume_mm3':v})
assert not collisions,collisions
# Contact areas of actual mating planar faces; no simulated force calculation.
upper=parts[0]['shape'];lower=next(x['shape'] for x in parts if x['group']=='lower_top')
def contact_area(a,b):
 total=0
 for f in a.Faces:
  for g in b.Faces:
   if f.BoundBox.intersect(g.BoundBox):total+=f.common(g).Area
 return total
bearings={x['id']:contact_area(x['shape'],upper) for x in parts if x['group']=='leg'}
shelf_bearings={x['id']:contact_area(x['shape'],lower) for x in parts if x['group']=='x_rail' and 'level 1 ' in x['name']}
assert sum(v>0 for v in bearings.values())==4 and all(v>0 for v in shelf_bearings.values())
# Export native named solids and an exact STEP assembly.
doc=App.newDocument('TB001_D07')
objects=[];mesh=[]
for item in parts:
 obj=doc.addObject('PartDesign::Feature',item['id']);obj.Label=item['id']+' '+item['name'];obj.Shape=item['shape']
 for key,val in [('Material',item['material']),('Role',item['group']),('Grain',item['grain']),('Evidence','ASSUMED / L1 / not for production')]:
  obj.addProperty('App::PropertyString',key,'Design');setattr(obj,key,val)
 if obj.ViewObject:obj.ViewObject.ShapeColor=(.9,.84,.71) if item['material']=='MAPLE' else (.39,.26,.18)
 objects.append(obj)
 vertices,faces=item['shape'].tessellate(.35)
 bb=item['shape'].BoundBox
 mesh.append({k:v for k,v in item.items() if k!='shape'}|{'vertices_mm':[[v.x,v.y,v.z] for v in vertices],'faces':[list(f) for f in faces], 'origin_mm':[bb.XMin,bb.YMin,bb.ZMin],'size_mm':[bb.XLength,bb.YLength,bb.ZLength],'volume_mm3':item['shape'].Volume})
doc.recompute();doc.saveAs(str(OUT/'TB001_D07.FCStd'));Import.export(objects,str(OUT/'TB001_D07.step'))
# Reopen the native artifact independently as well as STEP.
App.closeDocument(doc.Name)
reopened=App.openDocument(str(OUT/'TB001_D07.FCStd'))
native=[o for o in reopened.Objects if hasattr(o,'Shape')]
assert len(native)==len(parts) and all(o.Shape.isValid() for o in native)
assert abs(sum(o.Shape.Volume for o in native)-sum(x['shape'].Volume for x in parts))<.001
App.closeDocument(reopened.Name)
# Empty grip bore and unperforated lower centre, tested against actual solids.
probe=rr(L,W,r,zt+.01,tt-.02)
assert sum(x['shape'].common(probe).Volume for x in parts)<.001
assert abs(lower.Volume-math.pi*(p['shelf_diameter']/2)**2*p['shelf_thickness'])<.001
check=Part.read(str(OUT/'TB001_D07.step'));volume=sum(x['shape'].Volume for x in parts)
assert len(check.Solids)==len(parts) and abs(check.Volume-volume)<.01
(OUT/'geometry_mm.json').write_text(json.dumps({'revision':'D07','units':'mm','source':'Exact FreeCAD BRep tessellation, not AI','parts':mesh},ensure_ascii=False,separators=(',',':'))+'\n')
import tb001_three_tier as exporter
exporter.PARTS=mesh;exporter.OUT=OUT;exporter.REV='D07';exporter.COLORS={'MAPLE':'#e5d6b5','WALNUT':'#63432e'};exporter.glb()
checks={'status':'PASS — geometry only, not structural certification','solid_count':len(parts),'all_solids_valid':True,'native_readback_valid':True,'grip_bore_empty':True,'lower_full_disk_volume_verified':True,'positive_volume_collisions':collisions,'step_readback_solid_count':len(check.Solids),'step_volume_delta_mm3':check.Volume-volume,'upper_bearing_area_mm2':bearings,'lower_bearing_area_mm2':shelf_bearings,'x_bottom_z_top_to_bottom_mm':zs,'x_height_mm':h,'x_clear_gap_mm':h,'x_stack_height_mm':5*h,'grip_net_mm':[L,W],'grip_corner_radius_mm':r,'lower_has_grip':False,'shelf_to_leg_radial_clearance_mm':R-t/2-p['shelf_diameter']/2,'not_checked':['strength','tipping','carrying','wood movement','glue joint strength','pin tolerances','positive top/shelf retention','foot joinery']}
(OUT/'model_checks.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
with (OUT/'parts.csv').open('w') as f:
 writer=csv.writer(f);writer.writerow(['ID','Part','Material','Role','Global AABB mm — NOT blank size','Volume mm3','Grain'])
 for x in mesh:writer.writerow([x['id'],x['name'],x['material'],x['group'],' × '.join(f'{v:.2f}' for v in x['size_mm']),round(x['volume_mm3'],2),x['grain']])
print(json.dumps(checks,indent=2,ensure_ascii=False))
