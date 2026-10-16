from pathlib import Path
p=Path(__file__).resolve().parents[1]/'output'
s=['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1180" viewBox="0 0 1400 1180"><style>text{font-family:Arial,'PingFang TC',sans-serif;fill:#233142} .title{font-size:27px;font-weight:bold}.h{font-size:20px;font-weight:bold}.t{font-size:16px}.small{font-size:13px}.wood{fill:#b78a63;stroke:#553c29;stroke-width:1.5}.metal{fill:#ead5a4;stroke:#86672b;stroke-width:1.5}.dim{fill:none;stroke:#52728a;stroke-width:1} .dash{fill:none;stroke:#657a88;stroke-dasharray:5 4}</style><rect width="1400" height="1180" fill="#f7f8fa"/>''']
def text(x,y,t,cls='t'):s.append(f'<text x="{x}" y="{y}" class="{cls}">{t}</text>')
def rect(x,y,w,h,cls='metal',r=0):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}"/>')
def line(x,y,a,b,cls='dim'):s.append(f'<path d="M{x},{y} L{a},{b}" class="{cls}"/>')
def circle(x,y,r):s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f7f8fa" stroke="#526675"/>')
def dim(x,y,a,b,t):
 line(x,y,a,b);line(x-4,y-4,x+4,y+4);line(a-4,b-4,a+4,b+4);text((x+a)/2+7,(y+b)/2-7,t,'small')
text(45,47,'CB002 / D01   胡桃木 × 鋁板機箱','title');text(45,77,'CONCEPT — NOT FOR MANUFACTURE  /  尺寸 mm · 圖面不按比例列印 · 2026-10-12')
text(45,125,'01  前／後視：同外形，無元件孔','h')
sc=1.35;x=55;y=163
rect(x,y,520*sc,90*sc,'wood');rect(x+38*sc,y+13*sc,444*sc,64*sc,'metal',8*sc)
# hidden screw positions
for xx,zz in [(46,45),(474,45),(120,19),(120,71),(400,19),(400,71)]:
 circle(x+xx*sc,y+(90-zz)*sc,2.6);line(x+xx*sc-5,y+(90-zz)*sc,x+xx*sc+5,y+(90-zz)*sc,'dash')
dim(x,146,x+520*sc,146,'520 [A]');dim(780,y,780,y+90*sc,'90 [A]');text(55,314,'鋁板 444 × 64 × 6 / R8；小圓為背面盲孔位置，外表面不穿孔。','small')
text(45,370,'02  頂視：一定位孔＋五長孔（活動量待驗證）','h')
x=55;y=398;sc=1.2
rect(x,y,520*sc,380*sc)
for i,(xx,yy) in enumerate([(10,50),(10,190),(10,330),(510,50),(510,190),(510,330)]):
 if i==0:circle(x+xx*sc,y+yy*sc,2.25*sc)
 else:rect(x+(xx-3.75)*sc,y+(yy-2.25)*sc,7.5*sc,4.5*sc,'dim',2.25*sc)
dim(705,y,705,y+380*sc,'380 [A]');text(55,882,'顶板 520 × 380 × 4；固定點 X=10/510，Y=50/190/330。','small')
text(850,125,'03  面板固定剖面（放大示意）','h')
# y thickness across page: exterior left to interior right
rect(882,167,36,180,'metal');rect(918,167,84,180,'wood');rect(918,235,84,43,'dash')
# screw on solid shoulder; blind bore from back leaves 2 mm
rect(894,203,24,12,'dash');rect(900,205,108,8,'dim');rect(1002,194,6,30,'dim');rect(1008,196,12,26,'dim')
text(855,374,'外側 ← 鋁板6 / 木框20 → 內側','small');text(850,401,'M3×18 ＋ 1mm墊片；由內向外鎖。','small');text(850,425,'名義入牙3；底孔深4，孔底餘量1。','small');text(850,449,'鋁板背面抵木槽肩；不靠木螺絲固定。','small');text(850,473,'圖中螺紋省略；有效牙深須加工確認。','small')
text(850,535,'04  頂板固定剖面（放大示意）','h')
rect(890,631,140,112,'wood');rect(870,599,180,32,'metal');rect(940,631,40,80,'dim');rect(934,591,52,8,'dim');rect(942,568,36,23,'dim');rect(952,591,16,96,'dim')
text(850,775,'M4×12 ＋ 1mm墊片 → 木用M4嵌件。','small');text(850,800,'入牙7；嵌件外形暫示 Ø6×10。','small');text(850,825,'頂部螺絲可見；嵌件導孔依供應商。','small');text(850,850,'長孔暫沿X；實木活動方向須另驗證。','small')
line(45,925,1355,925)
text(45,963,'設計界線','h');text(45,997,'[K] 使用者轉述官方 52×38×23；暫按 cm 解讀。230 為整機參考高，不是木框高。')
text(45,1028,'[A] 圖示木框外形、板厚、孔位、固定件均為草案；木框90高依照片比例91±8選定。')
text(45,1059,'不含底板、腳座與元件；不做承重、散熱或電氣安全驗證。不得直接加工、載重或通電。')
text(45,1090,'裝配：木框膠合/木榫 → 由底部進工具鎖面板 → 裝嵌件 → 頂板定位、再鎖其餘螺絲。')
text(45,1140,'Sheet CB002-D01-01 / Concept assembly interface / Material grades, finish, tolerances &amp; checker: TBD','small')
s.append('</svg>');(p/'03_dimensions_and_fixings.svg').write_text('\n'.join(s))
