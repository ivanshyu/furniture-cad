# CB001 Curiosity Low · D16

[線上展示](https://ivanshyu.github.io/furniture-cad/CB001_D16_viewer.html)

- `reference/original_drawings/`：使用者提供的原廠 DWG / DXF。
- `models/D16/`：D16 Blender、GLB、3D網格DXF、幾何JSON、參數及互動網頁。
- `models/D16/gallery/`：AI效果、CAD底圖、分件圖、CSV及驗證報告。
- 專案根目錄 `scripts/*d16*`：D16建模、渲染、網頁及核對程式。

D16之前的方案保留本機，不同步。D16是外觀幾何方案；榫接、實物玻璃規格及製造开料尚未定案，詳models/D16/README.md。

## 重建
需要 Blender 4.5、Python 3與ezdxf。
1. `blender --background --python scripts/curiosity_d16_blender.py`
2. `blender --background --python scripts/d16_gallery_render.py`
3. `python scripts/d16_gallery_page.py`（包含逐件驗證）
4. `python scripts/publish_d16.py`（產生根目錄docs發布檔）

AI圖片已保留；上述重建不會重新呼叫AI。
