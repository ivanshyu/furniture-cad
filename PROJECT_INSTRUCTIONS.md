# Project Instructions

## 專案定位

本專案用於家具的研究、逆向重建、再設計、工程化與個人製作。目標不是只生成外觀相似的圖片，而是建立來源清楚、假設可追蹤、能交付打樣與製造評估的 production package。

## 不可違反的原則

1. **Reference 不是 Production Drawing。** 原廠照片、型錄、專利圖與舊圖紙只能作為證據來源。
2. **不得把推測偽裝成已知事實。** 所有關鍵尺寸、材料、結構與五金都必須標記證據狀態。
3. **先盤點證據，再重建幾何；先驗證結構，再出製造文件。**
4. **所有 `[ASSUMED]` 與 `[TO VERIFY]` 項目必須列入 open questions。** 未處理前不得標記為 L4。
5. **保留來源及權利狀態。** 不把「完全複製受保護原廠圖紙」設為專案目標。
6. **安全與可製造性優先。** 若外觀忠實度與強度、人體工學、設備限制或法規衝突，需記錄取捨並由人員確認。

## 證據狀態

- `[KNOWN]`：由可靠原始文件或實物量測直接取得。
- `[DERIVED]`：由已知基準、比例、幾何或多視圖推導；必須記錄算法與誤差。
- `[ASSUMED]`：依慣例、類似案例或製程暫定；必須說明理由。
- `[TO VERIFY]`：目前不能可靠判斷，或證據互相衝突。

格式範例：

```text
[KNOWN]   Overall width = 720 mm — catalog p.4
[DERIVED] Seat width = 438 ± 6 mm — front photo ratio, calibrated to overall width
[ASSUMED] Seat thickness = 25 mm — provisional machining stock
[TO VERIFY] Backrest inside radius ≈ R350 — perspective distortion too large
```

## AI 工作規則

AI 每一輪工作都應：

1. 說明本輪輸入與目標。
2. 區分觀察、推導、假設與未知。
3. 為推導值提供方法、基準、估計誤差及來源 ID。
4. 不用單張透視照片推導精密深度或角度。
5. 遇到證據衝突時保留多個候選值，不自行挑選成正式值。
6. 先更新 `evidence_register.md`、`dimensions.md`、`open_questions.md`，再更新圖紙與生產文件。
7. 在每次交付結尾列出：變更、可信度、未決問題、下一步與成熟度是否可升級。

## Production Candidate 最低內容

- Master spec 與 overall dimensions
- 零件編碼及 part drawings index
- BOM 與 cut list
- Joinery / hardware specification
- Assembly sequence
- Finish specification
- Tolerances 與 QC checklist
- 全部來源、假設、未決問題及 decision log

詳細規則見 `00_Project_Rules/`。
