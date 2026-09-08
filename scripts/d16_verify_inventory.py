# -*- coding: utf-8 -*-
from pathlib import Path
import json,csv,html,hashlib
from collections import Counter
import ezdxf
r=Path(__file__).resolve().parents[1]/'03_Cabinets/CB001_Curiosity_Low_Maple_Walnut/models/D16';g=r/'gallery'
data=json.loads((r/'geometry_mm.json').read_text());rows=list(csv.DictReader((g/'D16_parts_dimensions.csv').open(encoding='utf-8-sig')))
doc=ezdxf.readfile(r/'CB001_D16_3D_mesh.dxf');meshes=list(doc.modelspace().query('MESH'))
assert len(rows)==len(data['parts'])==len(meshes)==99
assert len({p['name'] for p in data['parts']})==99
assert not doc.audit().has_errors
materials={'WALNUT':'胡桃木','MAPLE':'楓木','GLASS':'長虹玻璃','METAL':'金屬'}
def dims(v):return [max(p[k] for p in v)-min(p[k] for p in v) for k in range(3)]
checks=[]
for i,(row,p,m) in enumerate(zip(rows,data['parts'],meshes)):
 d=dims(m.vertices);j=dims(p['vertices_mm']);expected=[float(row[k]) for k in ['x_mm','y_mm','z_mm']]
 assert row['id']==f'P{i+1:03}' and row['name']==p['name']
 assert row['material']==materials[p['material']] and m.dxf.layer==p['material']
 assert len(m.vertices)==len(p['vertices_mm'])
 assert max(abs(float(v[k])-p['vertices_mm'][n][k]) for n,v in enumerate(m.vertices) for k in range(3))<1e-6
 assert max(abs(d[k]-expected[k]) for k in range(3))<.001
 checks.append({'id':row['id'],'name':p['name'],'material':row['material'],'dimensions_mm':expected,'status':'PASS'})
parts={p['name']:p for p in data['parts']}
for p in parts.values():
 n=p['name'];target=None
 if n.startswith('POST') and n.endswith('upper'):target=[30,40,1105]
 if n.startswith('DOOR') and '_walnut_' in n:target=[22,32,1110] if n.endswith(('_L','_R')) else [286,32,22]
 if n.startswith('DOOR') and '_maple9_' in n:target=[9,12,1066] if n.endswith(('_L','_R')) else [268,12,9]
 if n.startswith('HANDLE') and n.endswith('_oval'):target=[24,24,39]
 if target:assert max(abs(x-y) for x,y in zip(dims(p['vertices_mm']),target))<.001
assert sum(n.startswith('POST') and n.endswith('upper') for n in parts)==4
assert sum(n.startswith('HANDLE') and n.endswith('_oval') for n in parts)==2
assert sum(n.startswith('HANDLE') for n in parts)==6
assert sum(n.endswith('GLASS') for n in parts)==4
assert sum(n.startswith('SHELF') for n in parts)==2
counts=Counter(row['group'] for row in rows)
report={'checks':checks,'group_mesh_counts':dict(counts),'handle_assemblies':2,'handle_meshes':6,'source_sha256':hashlib.sha256((r/'geometry_mm.json').read_bytes()).hexdigest(),'limitation':'Checks prove agreement between D16 model, exported DXF and CSV; not independent validation of manufacturing dimensions or source calibration.'}
(g/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
body='''<!doctype html><meta charset="utf-8"><title>D16 尺寸與數量驗證</title><style>body{font:16px system-ui;max-width:1100px;margin:32px auto;line-height:1.6}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:7px;text-align:left}</style><h1>D16 尺寸與數量驗證</h1><p>99／99 個模型分件通過：編號唯一、名稱一致、材質一致、DXF各頂點與模型一致、CSV尺寸與DXF外包絡誤差小於0.001 mm。DXF audit 無錯誤。</p><p>方法：另讀輸出的DXF網格逐件量測最大座標−最小座標，再比對CSV。另以尺寸公式檢查30×40×1105上柱、22＋9雙色門框、32門厚及24×24×39橢圓頭；數量規則檢查4上柱、4玻璃、2層板、2把手組。</p><p><b>驗證界線：</b>這證明模型、DXF和CSV彼此一致，不能證明原始設計假設或實物規格正確。原圖尺度仍按×5校準；尺寸為X/Y/Z組裝方向的外形包絡，不含榫頭、槽深、加工餘量。木腳色塊並非採購木料件數；玻璃4.6含模型起伏，並非訂購厚度。</p><h2>把手：2組，6個模型分件</h2><p>H01：P075橢圓頭、P076接頸、P077底座；H02：P087橢圓頭、P088接頸、P089底座。接頸和底座形狀是暫定模型。P071–P073為左門楓木飾條。</p><h2>GROUP模型分件數</h2>'''
body+='<ul>'+''.join(f'<li>{html.escape(k)}：{v}</li>' for k,v in counts.items())+'</ul><h2>逐件核對</h2><table><tr><th>編號</th><th>部件</th><th>材質</th><th>X × Y × Z mm</th><th>檢查</th></tr>'
body+=''.join('<tr><td>'+c['id']+'</td><td>'+html.escape(rows[i]['component'])+'</td><td>'+c['material']+'</td><td>'+' × '.join(map(str,c['dimensions_mm']))+'</td><td>通過</td></tr>' for i,c in enumerate(checks))+'</table>'
(g/'verification.html').write_text(body,encoding='utf8')
print('PASS: 99 parts; 2 handle assemblies / 6 meshes; independent DXF-to-CSV bounds <0.001mm')
