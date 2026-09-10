"""Publish the current D06 with a complete, non-stale six-view CAD/AI gallery."""
from pathlib import Path
import hashlib
import json
import shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'02_Tables/TB001_D16_Three_Tier/models/D06'
DESTINATION=ROOT/'docs/tb001'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_gallery(source):
    g=source/'gallery';m=json.loads((g/'ai_manifest.json').read_text())
    assert m['geometry_sha256']==digest(source/'geometry_mm.json'),'Regenerate AI after geometry changes'
    assert m['cad_manifest_sha256']==digest(g/'cad_manifest.json'),'CAD camera manifest changed'
    prompts=json.loads((g/'prompts.json').read_text())
    views=json.loads((source/'views.json').read_text())
    cad=json.loads((g/'cad_manifest.json').read_text())
    assert cad['geometry_sha256']==m['geometry_sha256'],'CAD geometry changed'
    assert set(m['views'])==set(views)==set(cad['views']),'All six views required'
    for key,entry in m['views'].items():
        assert cad['views'][key]['camera']==views[key],f'Camera changed {key}'
        assert cad['views'][key]['cad_sha256']==entry['input_sha256'],f'CAD source mismatch {key}'
        assert entry['input_sha256']==digest(g/f'{key}_cad.png'),f'Stale CAD {key}'
        assert entry['output_sha256']==digest(g/f'{key}_ai.png'),f'Unreviewed AI {key}'
        assert entry['prompt_sha256']==hashlib.sha256(prompts[key].encode()).hexdigest(),f'Prompt changed {key}'
    return m

def main():
    m=validate_gallery(SOURCE)
    DESTINATION.mkdir(parents=True,exist_ok=True)
    for src,dst in [('TB001_D06_viewer.html','index.html'),('preview.svg','preview.svg'),('preview.svg.png','preview.svg.png'),('TB001_D06.glb','TB001_D06.glb'),('parts_dimensions.csv','parts_dimensions.csv')]:
        shutil.copy2(SOURCE/src,DESTINATION/dst)
    g=DESTINATION/'gallery';g.mkdir(exist_ok=True)
    for name in ['ai_prompt.txt','prompts.json','ai_manifest.json','cad_manifest.json']+[f'{v}_{kind}.png' for v in m['views'] for kind in ['cad','ai']]:shutil.copy2(SOURCE/'gallery'/name,g/name)
    print('Built D06 and complete six-view gallery.')
if __name__=='__main__':main()
