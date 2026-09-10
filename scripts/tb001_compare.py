"""Same cameras/materials for 2 vs 1 line; rebuild core slots, don't hide bars."""
import copy
import hashlib
import json
from PIL import Image,ImageDraw,ImageFont
import tb001_d06 as model
import tb001_gallery_render as render
OUT=model.OUT
G=OUT/'gallery'

def main():
    manifest={'geometry_sha256':hashlib.sha256((OUT/'geometry_mm.json').read_bytes()).hexdigest(),'variants':{}}
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',26)
    sheet=Image.new('RGB',(1800,1120),'#f4f0e8');draw=ImageDraw.Draw(sheet)
    for i,n in enumerate([2,1]):
        model.build(n);checks=model.verify()
        render.DATA={'parts':copy.deepcopy(model.base.PARTS)}
        path=OUT/f'comparison_{n}_geometry.json'
        path.write_text(json.dumps({'revision':'D06','variant_line_count':n,'parts':render.DATA['parts']},separators=(',',':')))
        for view in ['persp','side']:
            im=render.render(model.VIEWS[view]);im.save(G/f'compare_{n}_{view}_cad.png')
            if view=='persp':sheet.paste(im,(i*900,100))
        draw.text((i*900+45,24),f'{n} LINE'+('S / CURRENT' if n==2 else ' / STUDY'),font=font,fill='#403329')
        draw.text((i*900+45,59),'Same maple / same camera / both keep main bearers',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20),fill='#776754')
        manifest['variants'][str(n)]={'geometry':'../'+path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':checks}
    sheet.save(G/'line_comparison_cad.png')
    model.build()
    render.DATA={'parts':[p for p in model.base.PARTS if p['role'] not in ['raised_panel','plywood_core','perimeter_strip']]}
    render.render(model.VIEWS['persp']).save(G/'supports_cad.png')
    manifest['assets']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [G/'supports_cad.png',G/'line_comparison_cad.png']+[G/f'compare_{n}_{v}_cad.png' for n in [1,2] for v in ['persp','side']]}
    (G/'comparison_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
