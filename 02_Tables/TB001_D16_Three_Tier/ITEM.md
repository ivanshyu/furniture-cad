# TB001 — Round Arch / Double Bands

## 目前主版
採用上板Ø650、下板Ø520、總高550／下層面高300 mm；四腳全厚雙胡桃橫段，條高與間隔14 mm。主檔目前位於 [D07 雙橫段目錄](models/D07/variants/upper_double_lines/README.md)，含七視角 AI／CAD。GitHub Pages 茶几主入口對應此版，D06方形版保留歷史入口。L1，承重與段間接合未定案。

## 以下為歷史演進紀錄（不代表目前主版）


- **目前：D07 Round Arch CAD 初稿**，僅上板開小孔；[原生 CAD 與工程待辦](models/D07/README.md)／[互動檢視](models/D07/TB001_D07_viewer.html)。
- **D06 為歷史矩形方案**，以下 D06 尺寸与構造不適用於 D07。
- **成熟度：L1**；外形及名義承托／槽口／半搭接已建立，承重與製造公差未驗證。
- 外廓 600 × 480 × 600 mm；面高 92 / 338 / 600 mm。
- D04 三明治直腳 + D05 倒角雙層托盤輪廓。
- 中／下層採兩道出頭承托線（12 mm 留白、10 mm 出頭），兩根橫托半搭接到左右側條，再穿入腿芯槽。
- 底板改四周胡桃木條＋夾板芯，上層楓木貼皮夾板；不使用整片胡桃木墊底。
- [設計與待驗證項目](design/D06_revision.md)
- [互動模型](models/D06/TB001_D06_viewer.html)
- [承托／省料圖解](models/D06/construction.html)
- [幾何檢查](models/D06/model_checks.json)
- [AI 共用 prompt](models/D06/gallery/ai_prompt.txt) · [逐視角 prompts](models/D06/gallery/prompts.json)

此前 D06「D05 + 2 條裝飾線」不再代表目前設計；歷史僅留於 Git。Reference → Engineering → Production，不得將 AI 圖當成尺寸／接合證據。

最新：三條版已取消，主版兩條；附一條 CAD 比較。楓木乳白淡紋，非橡木。

## 未定案造型探索
- [S01 · 板式支撐／橢圓桌面／拱形鏤空](studies/S01_Planes_And_Curves/README.md)：L0 AI 研究稿，不取代目前 D06。

- [S02 · 圓桌／楓木拱頂板腳／胡桃木框縫](studies/S02_Round_Arch_Maple/README.md)：最新兩層造型研究，D06 未替換。

- [S03 · 四腳／三層水平 X／開底槽與胡桃木腳墊](studies/S03_Four_Legs_Triple_X/README.md)：最新使用者修正，取代 S02 的兩腳研究方向；D06 不變。

## 最新造型基準候選
- [S04 · 緊密三層X／全楓木實木圓桌面](studies/S04_Compact_X_Solid_Maple/README.md)：使用者表示架構接近定案。淨間隙＝桿高；上下圓板皆楓木實木、無胡桃木弧邊、無貼皮。
- 造型基準：S04 + S05 上板單孔；CAD 已進入 D07。公開 Pages 仍是舊 D06，未同步發布。不得混用。

- [S05 · 桌面矩形框孔兩款微調](studies/S05_Rectangular_Grip_Studies/README.md)：①上桌面；②上下桌面。外觀比較，未替換S04基準；下層手指淨空與X交叉干涉待查。

## D07 CAD 初稿 · 2026-09-10
- 僅上桌面淨開孔暫定 95 × 30 mm／內外直角 R0，胡桃框寬 14 mm（對齊 X 桿高），必須實體試握。下板不開孔。
- 四腳、三組水平 X；桿高與淨間隔皆 14 mm；雙實木楓木圓板。所有數值為 ASSUMED。
- 44 個有效 BRep 零件及 STEP 回讀通過幾何檢查；非承重／可製造化認證。
- 桌板正向固定、腳墊榫接、木材伸縮及穿銷強度仍待完成，不得透過桌面孔提起整桌。

- D07 最新比例：Ø650 × H550；下板 Ø450／面高300，板間淨高230 mm。已取代 Ø700 × H500 矮寬試版，歷史参数及預覽另存。低視角從兩隻前腳之間看進去。

## 上方雙橫線試款
- [獨立 CAD 試款](models/D07/variants/upper_double_lines/TB001_D07_viewer.html)：每腳外側兩條胡桃木橫飾條，14 mm高／14 mm間隔，4 mm深齊平嵌入，距拱冠起點26 mm（整組下移20 mm）。基準D07與六視角AI不變，試款尚未AI渲染。

- 雙橫線最新：再下移50 mm，距拱冠起點76 mm，改為20 mm全厚胡桃木橫段，楓木脚被截成三段。非淺嵌條，承重接合未設計。

- 雙橫段試款最新：下層Ø520、腳中心半徑275，其餘高度及上板Ø650不變；X桿586 mm。基準版D07與其AI仍維持Ø450，請勿混用。