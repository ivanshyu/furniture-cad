# D01 檢查紀錄 · 2026-09-10

- `python3 scripts/tb001_three_tier.py`：PASS。外包絡600×480×600 mm、三個面高140/350/600 mm、61個視覺分件。
- 全部分件正體積、閉合且面方向一致；所有成對軸對齊包絡交集檢查：0個正體積重疊。本模型均為方體，該檢查即實際相交檢查。
- GLB回讀：檔案長度、JSON區塊、61個mesh及所有bufferView範圍檢查PASS。單位為m，Y向上；來源JSON以mm、Z向上。
- 瀏覽器實測：61個分件正常呈現；正面／立體按鈕、分層展開0→1→0、P045選件498×358×18 mm顯示PASS。
- 立體外觀與SVG尺寸板人工目視檢查完成。SVG為幾何投影，非材質實拍；GLB與互動頁用純色近似木材。
- `git diff --check`：PASS。

Geometry confidence: High（相對本輪設計參數）；Construction / Materials: Low（未打樣、樹種與工法待確認）。
Current maturity: L1。L1外觀方案PASS；L2工程化HOLD，未定義榫接、面板托持及實木活動量。
幾何檢查不代表物理連接、側向剛性或承重已驗證。零件表為視覺分件外形，不是採購數量或cut list。
下一步：以本模型確認外觀與使用高度，完成接合細節及原型驗證。
