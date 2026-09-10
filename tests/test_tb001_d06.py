"""Envelope, actual bearing path, line variants, material and publication regressions."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import tb001_d06 as model
import publish_tb001

class D06Tests(unittest.TestCase):
    def setUp(self):model.build()
    def test_preserved_trays_maple_and_edge_only(self):
        checks=model.verify()
        self.assertEqual(checks['d05_raised_panels_unchanged'],3)
        self.assertEqual(len(model.base.PARTS),94)
        self.assertEqual({p['material'] for p in model.base.PARTS},{'WALNUT','MAPLE'})
        self.assertEqual(checks['dark_deck_material_mm3']['volume_reduction_percent'],80.4)
    def test_both_variants_have_real_bearers(self):
        for n in [1,2]:
            model.build(n);checks=model.verify()
            self.assertEqual(set(checks['load_paths']),{'Lower','Middle'})
            braces=[p for p in model.base.PARTS if p['role']=='through_brace']
            self.assertEqual(len(braces),4*(n-1))
            for p in braces:self.assertEqual((p['origin_mm'][1],p['size_mm'][1]),(2,476))
    def test_missing_bearer_fails_verification(self):
        model.base.PARTS=[p for p in model.base.PARTS if not (p['role']=='cross_bearer' and p['group']=='Lower')]
        with self.assertRaises(AssertionError):model.verify()
    def test_overlap_and_positive_area_contact(self):
        a=model.base.PARTS[0];self.assertTrue(model.overlap(a,a))
        b=copy.deepcopy(a)
        for v in b['vertices_mm']:v[0]+=1000
        self.assertFalse(model.overlap(a,b));self.assertFalse(model.contact(a,b))
        b=copy.deepcopy(a)
        for v in b['vertices_mm']:v[2]+=22
        self.assertTrue(model.contact(a,b));self.assertFalse(model.overlap(a,b))
    def test_gallery_hashes(self):
        m=publish_tb001.validate_gallery(model.OUT)
        self.assertEqual(set(m['views']),{'persp','front','side','top','detail','bottom'})
    def test_ui_materials_and_support_toggle(self):
        text=(model.OUT/'TB001_D06_viewer.html').read_text()
        self.assertIn('MAPLE:0xe5d6b5',text)
        self.assertNotIn('NATURAL_OAK:',text)
        self.assertIn('id="showSupports"',text)
        self.assertIn('objects.filter(o=>o.visible)',text)
        self.assertIn('controls.dispose()',text)
        self.assertIn(']??0)',text)
        self.assertIn('construction.html',text)
        for v in model.VIEWS:self.assertIn(f'data-view="{v}"',text)
    def test_published_gallery_matches(self):
        for v in model.VIEWS:
            for kind in ['ai','cad']:
                name=f'{v}_{kind}.png'
                self.assertEqual((model.OUT/'gallery'/name).read_bytes(),(ROOT/'docs/tb001/gallery'/name).read_bytes())
    def test_compare_default_is_current_geometry(self):
        expected=json.loads((model.OUT/'geometry_mm.json').read_text())['parts']
        actual=json.loads((model.OUT/'comparison_2_geometry.json').read_text())['parts']
        self.assertEqual(expected,actual)
        comparison=json.loads((model.OUT/'gallery/comparison_manifest.json').read_text())
        self.assertEqual(comparison['geometry_sha256'],publish_tb001.digest(model.OUT/'geometry_mm.json'))
if __name__=='__main__':unittest.main()
