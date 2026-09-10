"""Geometry preservation, convex-contact and publication completeness regression tests."""
import copy
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import tb001_d06 as model
import publish_tb001

class D06Tests(unittest.TestCase):
    def setUp(self):model.build()
    def test_d05_unchanged_and_two_lines(self):
        self.assertEqual(model.verify()['d05_base_parts_unchanged'],15)
        self.assertEqual(len(model.base.PARTS),17)
        self.assertEqual({p['material'] for p in model.base.PARTS},{'SMOKED_OAK','NATURAL_OAK'})
    def test_convex_contact_and_overlap(self):
        a=model.base.PARTS[0];self.assertTrue(model.overlap(a,a))
        b=copy.deepcopy(a)
        for v in b['vertices_mm']:v[0]+=1000
        self.assertFalse(model.overlap(a,b))
        # Added line meets, but does not penetrate, its two tapered leg faces.
        self.assertFalse(model.overlap(model.base.PARTS[0],model.base.PARTS[15]))
        self.assertFalse(model.overlap(model.base.PARTS[1],model.base.PARTS[15]))
    def test_gallery_hashes_and_all_views(self):
        m=publish_tb001.validate_gallery(model.OUT)
        self.assertEqual(set(m['views']),{'persp','front','side','top','detail','bottom'})
    def test_ui_materials_and_explode_fallback(self):
        text=(model.OUT/'TB001_D06_viewer.html').read_text()
        self.assertIn('SMOKED_OAK:0x594638',text)
        self.assertIn('NATURAL_OAK:0xc8aa7d',text)
        self.assertIn('Structure:0',text)
        self.assertIn('controls.dispose()',text)
        self.assertIn('controls=new OrbitControls(camera,renderer.domElement)',text)
        self.assertIn(']??0)',text)
        self.assertNotIn('Line & Plane',text)
        self.assertIn('prompts.json',text)
        for v in model.VIEWS:self.assertIn(f'data-view="{v}"',text)
    def test_published_gallery_matches(self):
        for v in model.VIEWS:
            for kind in ['ai','cad']:
                name=f'{v}_{kind}.png'
                self.assertEqual((model.OUT/'gallery'/name).read_bytes(),(ROOT/'docs/tb001/gallery'/name).read_bytes())
if __name__=='__main__':unittest.main()
