"""Build TB001 GitHub Pages files. Run after tb001_three_tier.py."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '02_Tables/TB001_D16_Three_Tier/models/D01'
DESTINATION = ROOT / 'docs/tb001'
DESTINATION.mkdir(parents=True, exist_ok=True)
for source_name, public_name in [
    ('TB001_D01_viewer.html', 'index.html'),
    ('preview.svg', 'preview.svg'),
    ('TB001_D01.glb', 'TB001_D01.glb'),
    ('parts_dimensions.csv', 'parts_dimensions.csv'),
]:
    shutil.copy2(SOURCE / source_name, DESTINATION / public_name)
print('Built TB001 Pages: https://ivanshyu.github.io/furniture-cad/tb001/')
