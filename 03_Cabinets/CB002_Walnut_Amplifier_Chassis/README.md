> **現行 D05（2026-10-16 已生成並通過幾何驗證）**：木框主體與內角補強柱（`CB01..CB04`）採**緬甸柚木（Burmese Teak）**，四角 **45° 斜角接合＋北美黑胡桃木雙羽鍵榫（`SP01..SP08`）**；前後木框為「外側 $444.6 \times 64.6 \times 4.0$ 嵌槽（**$6\text{ mm}$ 面板向外浮凸 $2.0\text{ mm}$**）＋內側加大為 **$404 \times 48 \times 16.0$** 貫通窗口＋周邊 **$16\text{ mm}$ 厚木肩**（$M3 \times 20$ 內鎖）」；頂板為**雙層階梯厚板（周邊 8＋上層內縮 10 厚 5＋下緣定位凸台 4，頂面無孔）**；**四面木框（左右各 3 組＋前後上橫樑各 2 組，共 10 組）均採上止口垂直盲槽預埋雙孔方螺母條＋內側 L 支架**；底部配 4 顆 $\varnothing 48 \times 14$ 金屬腳墊。成果位於 `output/D05/`（含 `CB002_D05.FCStd`、`CB002_D05_assembly.step`、25 個分件 STEP、`BOM.csv`、`validation.txt`、渲染圖與工程剖面圖 `03_dimensions_and_fixings.svg/.png`），詳見 [D05說明](design/D05_stepped_opening.md)。所有尺寸均為 `[ASSUMED]` / `[TO VERIFY]` 概念草案，成熟度維持 **L0 / L1 HOLD**，不得直接用於製造。下方為歷史紀錄。

> **現行試案 D04**：前後木框取消中央窗口；頂板改定位台階＋內側L支架、由下向上鎖，頂面無螺絲。檔案 `output/D04/`；詳細尺寸及未決事項見 [D04_hidden_top.md](design/D04_hidden_top.md)。下方為歷史紀錄。

> **現行版本 D03**：外側整片面板嵌槽＋內側螺絲鎖入鋁板背面。**D02螺絲頭沉孔方案已作廢**。成果位於 `output/D03/`；詳見 [D03剖面定義](design/D03_panel_rebate.md)。下方D01/D02敘述保留作歷史。

# CB002 胡桃木機箱 — D01 概念版

**CONCEPT — NOT FOR MANUFACTURE。成熟度 L0，L1 HOLD（官方包絡定義與木框尺寸未確認）。**

## 直接查看
- `output/01_assembled.png`：組裝外觀。
- `output/02_exploded.png`：同一 CAD 幾何之分解視圖。
- `output/03_dimensions_and_fixings.svg`：尺寸與固定剖面示意。
- `output/CB002_D01.FCStd`：FreeCAD 57件組立；各件為有效B-rep實體，非完整Sketcher特徵歷程。
- `output/CB002_D01_assembly.step`：通用CAD組立；另有7個主要零件STEP。
- `output/CB002_D01.blend`：含材質與燈光的Blender場景；木紋與金色鋁表面僅示意。
- `output/BOM.csv`、`output/validation.txt`：暫定物料表與幾何驗證。

## 本輪決策
官方52×38×23暫按cm，即520×380×230mm。230暫視為含頂部元件之高度；沒有把機箱做成230高。照片S03木框像素比例約165/943，若寬520，得91±8；先採90高。木框外包絡520×380×90、頂板4厚，外殼本體高94，不含腳座。

前後空白面板444×64×6、R8，金色鋁表面為外觀選擇，合金與處理未定。沒有端子、旋鈕或管座孔。保留必要固定孔：面板背面M3盲孔、頂板M4通孔/長孔。

## 固定與拆裝
1. 木框前後料沿X木紋、左右料沿Y；四角直角對接，每角2支Ø6×30木榫加膠。未復刻照片的疑似指接。膠種、榫配合及強度待驗證。
2. 前後面板從外側放入6mm深嵌槽；由開放底部伸入工具，12組M3×18與1mm墊片經木框鎖入鋁板背面盲牙。每板6點。外面不露螺絲；背面盲孔Ø2.5深4是簡化底孔，未建螺紋。需底攻取得至少3mm有效牙，嚴防鑽穿。可在鎖顶板前裝面板。
3. 頂板用6組M4×12及1mm墊片鎖入木框嵌件，名義入牙7mm。只有一圓形定位孔，其餘長孔；頂面螺絲可見。不可把長孔夾死而宣稱能自由伸縮，墊片與鎖緊方式需實測。
4. 嵌件外形OD6×10為占位模型，不是已選購五金；木材導孔須依實際嵌件規格重新建模與試裝。
5. 底板與腳座尚未設計，保留維修進入空間；不是可投入使用的完成機箱。承載骨架是否加入留待負載決定。

## 驗證與限制
57件形狀有效且體積正；7件主要木/鋁件無體積重疊。前後由同一幾何旋轉180°得到；螺絲長度与名義入牙量已核算。螺紋只用包絡/底孔表示，不做螺旋牙嚙合驗證。不包含加工公差、力學、散熱、接地與高壓安全認證。請勿依本稿直接下料或通電。

## 重建
主尺寸位於 `cad/build_chassis.py` 頂端。修改後執行（從專案根目錄）：

```sh
PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib \
/Applications/FreeCAD.app/Contents/Resources/bin/python \
03_Cabinets/CB002_Walnut_Amplifier_Chassis/cad/build_chassis.py
.tools/Blender.app/Contents/MacOS/Blender -b --python \
03_Cabinets/CB002_Walnut_Amplifier_Chassis/cad/render_chassis.py
```

FreeCAD的Master_Dimensions為紀錄，修改它不會自動驅動實體；請改腳本再生成。部分孔位仍為D01布局常數，大幅改尺寸需同步重審，不是任意尺寸都安全的設計器。SVG是D01標註快照，改尺寸後也須更新 `cad/draw_sheet.py`。

## 下一步
確認外觀比例、木框高度、頂部可見螺絲是否接受，再選鋁材/嵌件、修訂接點與活動量，最後才安排開孔、承載底架、腳座、底板與加工圖。原圖只保留本機，不上傳或發布。


## 最新 D02：內側沉孔＋短螺絲
使用者修正已套用，D01為歷史方案。現行檔案位於`output/D02/`，CAD名為`CB002_D02.FCStd`，STEP名為`CB002_D02_assembly.step`；其餘圖面同名。詳見[固定剖面與限制](design/D02_counterbore.md)。前後各6個Ø8深8平底沉孔，M3×10＋1mm墊片，夾持槽肩6mm、入鋁板3mm、頭藏5mm。頂板不變。
