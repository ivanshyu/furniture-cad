# Standard Workflow

## 0. Intake

- 建立 item 目錄並填寫 `ITEM.md`。
- 記錄用途、忠實度目標、材料偏好、設備能力、預算及權利狀態。
- 原始附件只放進 `reference/`；避免覆寫原檔。

## 1. Evidence Audit — L0

- 在 `reference/sources.md` 為每個來源建立唯一 ID。
- 提取可直接確認的尺寸、視角、材質、年代與結構線索。
- 在 `research/evidence_register.md` 登錄證據、可信度與限制。
- 回報缺少的視角或量測。

## 2. Reconstruction — L1

- 選擇至少一個可靠尺寸作為比例基準。
- 校正透視及鏡頭變形後再量比例。
- 交叉比對正、側、後、俯、底視圖。
- 將結果寫入 `design/dimensions.md`，保留誤差範圍。

## 3. Engineering — L2

- 建立零件分解、材料、木紋方向、榫接、五金與受力路徑。
- 檢查人體工學、材料收縮、加工基準、刀具可達性與裝配空間。
- 在 `design/risk_review.md` 記錄風險與需試驗項目。

## 4. Prototype Package — L3

- 完成第一版圖紙索引、BOM、cut list、joinery、assembly 與 finish spec。
- 明確標示非最終尺寸及原型驗證點。
- 製作 1:1 關鍵接點樣件或整體原型，回填實測結果。

## 5. Production Release — L4

- 關閉所有影響安全、裝配或外觀的 open questions。
- 將所有 `[ASSUMED]` 轉為已驗證狀態，或由負責人簽核為明示設計決策。
- 凍結 revision，執行 QC checklist，輸出 production package。

## 每輪 AI 回報格式

```text
Work completed
Evidence added/changed
Confidence: Geometry __% / Construction __% / Materials __%
Open questions
Risks
Recommended next action
Current maturity: L_
Gate result: PASS / HOLD
```
