"""Build TB001 D06 GitHub Pages files. Run after tb001_d06.py."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '02_Tables/TB001_D16_Three_Tier/models/D06'
DESTINATION = ROOT / 'docs/tb001'
DESTINATION.mkdir(parents=True, exist_ok=True)
for source_name, public_name in [
    ('TB001_D06_viewer.html', 'index.html'),
    ('preview.svg', 'preview.svg'),
    ('preview.svg.png', 'preview.svg.png'),
    ('TB001_D06.glb', 'TB001_D06.glb'),
    ('parts_dimensions.csv', 'parts_dimensions.csv'),
]:
    shutil.copy2(SOURCE / source_name, DESTINATION / public_name)
(DESTINATION / 'gallery').mkdir(exist_ok=True)
shutil.copy2(SOURCE / 'gallery/persp_ai.png', DESTINATION / 'gallery/persp_ai.png')
print('Built TB001 Pages: https://ivanshyu.github.io/furniture-cad/tb001/')
