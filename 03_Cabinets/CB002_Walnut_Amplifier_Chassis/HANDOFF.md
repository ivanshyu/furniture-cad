# CB002 CAD 接手說明（2026-10-16）

## 先讀

1. 專案根目錄 `PROJECT_INSTRUCTIONS.md`、`WORKFLOW.md`：證據標記與成熟度門檻。
2. 本目錄 `README.md`、`ITEM.md`、`design/dimensions.md`、`design/open_questions.md`、`design/decision_log.md`。
3. 最新需求：`design/D05_stepped_opening.md`；頂板固定：`design/D04_hidden_top.md`。
4. 四張原始參考：`reference/1-照片-1.jpg` 至 `reference/4-照片-4.jpg`，來源限制見 `reference/sources.md`、`research/evidence_register.md`。

## 當前狀態（2026-10-16 已完成 D05 生成、幾何強化與驗證）

- **最新完整生成與驗證版為 D05**：位於 `output/D05/`，已完整產出 `CB002_D05.FCStd`、`CB002_D05_assembly.step`、25 個分件 STEP（W01–W04、A01–A03、F01–F04、CB01–CB04、LB0–RB2、FB0–BB1）、`BOM.csv`、`validation.txt`、組裝渲染 `01_assembled.png`、爆炸視圖 `02_exploded.png`、工程剖面與尺寸圖 `03_dimensions_and_fixings.svg/.png`、底部固定檢視 `04_underside_fixings.png` 與裸木框二級鏤空檢視 `05_stepped_wood_frame.png`。
- **本輪 D05 針對原廠照片（S01–S04）與使用者指定材質／結構之優化**：
  1. **前後面板浮凸 $2\text{ mm}$ ＋ 加大 $404 \times 48\text{ mm}$ 貫通接線窗**：第一級外側 $444.6 \times 64.6 \times 4.0$（$R8.3$）嵌槽放入 $444 \times 64 \times 6$ 倒角面板（**面板嵌入 $4\text{ mm}$、向外浮凸於木框完成面 $2\text{ mm}$**）；第二級中央貫通窗口高度由 $40\text{ mm}$ **加大至 $48.0\text{ mm}$**（$404 \times 48 \times 16.0$，$R6.0$），以容納 ALPS RK50 與表頭；四周保留加厚至 **$16.0\text{ mm}$** 之實木肩（左右寬 $20\text{ mm}$、上下寬 $8\text{ mm}$），由機內 6 組 $M3 \times 20$ 穿過木肩鎖入面板背面盲牙。
  2. **緬甸柚木框 ＋ 北美黑胡桃 45° 斜角雙羽鍵榫 ＋ 內部實木補強角柱**：主框（`W01..W04`）與 4 支 $22 \times 22 \times 78\text{ mm}$ 內角補強柱（`CB01..CB04`）採 **緬甸柚木（Burmese Teak）**，四角 45° 斜接並嵌入 8 片 $14 \times 14 \times 5\text{ mm}$ **北美黑胡桃木（American Black Walnut）** 三角形羽鍵（`SP01..SP08`，$Z=21..26$ 與 $Z=64..69\text{ mm}$）。
  3. **四面木框 10 點上止口垂直盲槽預埋雙孔方螺母條（All-4-Wall Top-Drop Square Nut Bars）**：還原照片 S04（ALPS RK50 正上方之前木框預埋螺母），除左右側壁各 3 組（`LB0..RB2`）外，**前後木框上橫樑（$X=185, 335$，$Z=69..90\text{ mm}$）亦增設各 2 組上止口盲槽預埋雙孔方螺母條（`FB0..BB1_SquareNutBar`，$20 \times 14 \times 4\text{ mm}$）與 $16\text{ mm}$ 高緊湊型 L 支架（$Z=70..86\text{ mm}$，完全不遮擋 $48\text{ mm}$ 窗口）**，將前後細木樑直接鎖固於 $13\text{ mm}$ 厚金屬頂板。
  4. **雙層階梯頂板与底部腳墊**：下層外周 $8\text{ mm}$＋上層內縮 $10\text{ mm}$ 厚 $5\text{ mm}$＋底部定位凸台 $4\text{ mm}$，頂面 100% 無外露螺絲孔；底部配 4 顆 $\varnothing 48 \times 14\text{ mm}$ 車削金屬腳墊。
- **所有尺寸仍為 `[ASSUMED]` / `[TO VERIFY]` 概念草案**，成熟度維持 **L0 / L1 HOLD**，不得當作原廠尺寸或加工定稿。

## 接手任務

1. 對照 D05 腳本與剖面確認兩級木槽、木肩與六個前後板固定點的幾何；特別檢查腳本能否通過內窗口和承壓木肩的驗證。
2. 執行 D05 FreeCAD 腳本，輸出 FCStd、STEP、分件 STEP、BOM、validation；再重新渲染組裝、爆炸、底部固定與裸木框視圖。未成功執行時不要發佈 D05 模型。
3. STEP 回讀與形狀合法性、非螺紋零件干涉、面板螺絲及頂板工具通道再次確認；檢查圖面標註與模型一致。
4. 將所有草案尺寸繼續標記 `[ASSUMED]` / `[TO VERIFY]`；未有元件後部包絡、載重、散熱與電氣資訊前，不可出加工定稿或宣稱安全。

## 本機執行提示

FreeCAD 位於 `/Applications/FreeCAD.app`，Blender 位於專案 `.tools/Blender.app`。過去用 `PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib /Applications/FreeCAD.app/Contents/Resources/bin/python cad/build_chassis_d05.py`（請自專案根目錄使用完整相對路徑）。在沙箱中 FreeCAD/Blender 可能因 Qt/CPU 特性無法啟動；若執行需系統審核且被拒，尊重限制、記錄未完成狀態，不繞過審核。

## 權利與成熟度

商業產品照片僅供本機研究，權利狀態未查證，不擅自公開。此專案仍為 L0/L1 HOLD；所有固定、材料、螺紋、承重與公差須實物或樣件驗證。
