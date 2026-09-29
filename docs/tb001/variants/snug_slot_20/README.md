# 20 mm 滿槽外觀試版

基於下層Ø520、上板Ø650、高550的雙橫段版。修改：槽邊胡桃木條可見寬4、厚20；槽內淨寬20；三組X桿截面20 × 20，桿間淨距20。維持下層板底標高280，因此X底標高260／220／180。腳內原始開口為28，剩餘兩側楓木各46。橫桿完整截面填滿槽寬，沒有縮頸榫，取消12支穿銷及其所有孔。中央半搭接保留。出頭仍8 mm，非齊平截短。

上方手孔淨空95 × 30不變，框依既有與X桿同寬規則同步改20（外廓135 × 70）；上方兩道貫穿胡桃木段仍14高／14間隔，位置不變。

名義零側隙只是外觀，非製造公差。取消穿銷後，只剩側面接觸：側面填滿並不提供可靠向下承托，固定與荷載傳遞未設計。不能假定靠摩擦或膠合就安全。上桌面、分段腳與腳墊接合亦未完成。L1造型稿，非施工圖，不代替既有主版。已提供七個視角的 AI／Blender 對照。

重建時設定TB001_D07_OUT為本資料夾，使用FreeCAD Python執行scripts/tb001_d07_freecad.py，再用Python執行展示與尺寸圖腳本。

## 最新修正：鏤空框條還原
僅將腳槽周圍胡桃木框條可見寬由20還原為4 mm，厚度20不變。槽淨寬與X桿截面仍20／20 × 20 mm，仍無穿銷。腳內原始開口改為28 mm，兩側楓木各46 mm。上桌面孔框20、上方雙橫段14皆未改動。以上取代先前20 mm腳槽框條描述。

## Blender 材質階段（2026-09-11）

FreeCAD `.FCStd`／STEP 仍是尺寸來源。`TB001_D07_materials.blend` 匯入本版 `geometry_mm.json` 的全部零件，保留頂點位置；只設定程序木紋、平滑法線、相機與棚燈。無新增倒角或重新建模、無AI生成。材質表達為乳白楓木與深胡桃木；程序木紋不代表實際選料／塗裝。

七個相機對應 `views.json`，輸出 `gallery/*_blender.png`；可在互動頁切換「AI 渲染／Blender 底圖」。底視隱藏攝影棚地板；承托圖隱藏兩片桌板，其餘不變。`gallery/blender_manifest.json` 保存源幾何、相機、腳本、圖檔與場景雜湊。

重建：
```sh
.tools/Blender.app/Contents/MacOS/Blender --background --python scripts/tb001_blender_render.py
TB001_D07_OUT="$PWD/02_Tables/TB001_D16_Three_Tier/models/D07/variants/snug_slot_20" python3 scripts/tb001_d07_present.py
```
Blender 4.5.3 ARM64 自官方下載後置於忽略版控的 `.tools/Blender.app`，未安裝到系統 Applications。此階段改善視覺，不提升結構成熟度；滿槽無穿銷、分段腳等承重接合仍未設計。

### AI / Blender 對照更新

七張 AI 材質圖以本版各視角的 Blender PNG 為編輯底圖，使用內建 image_gen 重新生成，未沿用前版 AI 圖。圖庫預設 AI，可切換 Blender 底圖；CAD 保留上方互動視窗。

- 提示詞：`gallery/ai_prompts_blender_v1.json`
- AI 圖：`gallery/*_ai_v1.png`
- 來源與雜湊：`gallery/ai_blender_manifest_v1.json`
- 已目視檢查七視角、雙橫段、三層 X、方形開孔與主要遮擋；AI 細節與木色仍有偏差，不代表加工圖或真實木料。
- 本次僅更新本機與 docs 鏡像，未推送部署。
