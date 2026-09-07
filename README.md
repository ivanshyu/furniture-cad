# Furniture Engineering / Reproduction Project

這是一套把家具參考資料逐步轉換為可驗證、可打樣、可製造文件的專案骨架。

核心資料流：

```text
Reference → Reconstruction → Engineering → Prototype → Production Ready
```

## 目錄

```text
00_Project_Rules/   全專案共用規範、材料與五金資料庫
01_Chairs/          椅類項目
02_Tables/          桌類項目
03_Cabinets/        櫃類項目
90_Templates/       新家具項目的標準模板
PROJECT_INSTRUCTIONS.md
WORKFLOW.md
```

## 建立新家具項目

1. 執行下列指令，或手動複製 `90_Templates/ITEM_TEMPLATE/` 到適當分類。

   ```bash
   python3 scripts/new_item.py 01_Chairs CH001 Wood_Chair
   ```

2. 依 `{類別代碼}{流水號}_{簡短名稱}` 命名，例如 `CH001_Wood_Chair`。
3. 先填 `ITEM.md`、`reference/sources.md` 與 `research/evidence_register.md`。
4. 未完成證據盤點前，不建立正式生產尺寸。
5. 依 `00_Project_Rules/MATURITY_GATES.md` 升級成熟度。

所有尺寸預設使用 **mm**。正式文件中的每項關鍵尺寸都必須附有證據狀態。
