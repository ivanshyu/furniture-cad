# Drawing Rules

## 圖紙識別

- 圖號建議：`{ITEM}-{PART}-{SHEET}`，例如 `CH001-A01-01`。
- 每張圖應包含 item、part name、part number、revision、date、scale、units、material、finish、drafter/checker。

## 尺寸與公差

- 不重複標註同一控制尺寸。
- 尺寸應從功能 datum 標註，不依未定義邊緣累積鏈式誤差。
- 一般與關鍵公差必須分開；配合、榫接、孔距與對稱度需明示。
- 所有 derived/assumed 尺寸在 L3 前仍需於尺寸表保留狀態；L4 圖紙只使用已批准值。

## Revision

- 草案：`D01`, `D02`…
- 原型：`P01`, `P02`…
- 生產發布：`R01`, `R02`…
- 任何會影響互換性、外觀、材料、強度或裝配的變更都必須寫入 decision log。
