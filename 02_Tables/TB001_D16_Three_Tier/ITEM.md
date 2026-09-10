# TB001 · Quiet Frame / Fine Lines 三層邊几

Revision D06（重做）· 2026-09-10 · L1 外觀幾何方案

這版 D06 直接以 D05 為基底，不是先前被否決的 Line & Plane。
D05 全部 15 個模型分件、材料與頂面／中層／下層高度原樣保留，只加入左右各一道細橫線，合計 17 個視覺分件。

- 外廓：600 × 480 × 600 mm，沒有出頭。
- 三層面高：92 / 338 / 600 mm。
- 材質提案：煙燻橡木腳、框與細線；自然橡木嵌面。
- 新側線：8 × 10 mm，下緣離地 370 mm，距中層表面 32 mm。
- 四腳保留 D05 的上端 34 × 38、下端 26 × 30 mm 錐形截面。
- 幾何接觸、封閉網格與無干涉不代表接合或承重已通過驗證；層板托持仍未設計。

## 檢視

- [D06 互動模型與六視角 CAD／AI 對照](models/D06/TB001_D06_viewer.html)
- [D05 原始方案](models/D05/TB001_D05_viewer.html)
- [完整尺寸參數](models/D06/parameters.json)
- [更新說明](design/D06_revision.md)
- [共用 AI prompt](models/D06/gallery/ai_prompt.txt)
- [六個完整 prompts](models/D06/gallery/prompts.json)
- [產圖及 QA manifest](models/D06/gallery/ai_manifest.json)

AI 視角：透視、正面、左側、俯視、側線接點、底部；每張使用對應 CAD 底圖，不以 AI 圖推回幾何。沒有把手，因此不沿用 D16 的 handles 視角。

## 重建

```bash
python3 scripts/tb001_d06.py
python3 scripts/tb001_gallery_render.py
python3 scripts/publish_tb001.py
```

Python 依賴：NumPy、Pillow。上列指令不呼叫 AI、不花費 API 費用；AI 另由內建 ImageGen 依 prompts.json 執行。
如修改幾何，須重新產六張 AI 圖，更新 hash 與 QA；發布腳本拒絕過期的 AI manifest。

原先 D06 寬板腿方案已由本版覆寫，不在總覽或版本列表另留入口；Git 正常提交歷史不改寫。
歷史 D01–D04 保留作研究紀錄，不是本版尺寸來源。
