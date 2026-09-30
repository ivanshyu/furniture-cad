"""Static contract against the shipped cabinet; browser checks recorded separately."""
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ViewerParity(unittest.TestCase):
 def test_cabinet_controls_present(self):
  cabinet=(ROOT/'docs/CB001_D16_viewer.html').read_text()
  chair=(ROOT/'docs/mc10/index.html').read_text()
  ids=set(re.findall(r'id="([^"]+)"',cabinet))
  self.assertTrue(ids.issubset(set(re.findall(r'id="([^"]+)"',chair))),ids-set(re.findall(r'id="([^"]+)"',chair)))
 def test_scope_disclosed(self):
  chair=(ROOT/'docs/mc10/index.html').read_text()
  for text in ['非原廠 BOM','玻璃（不適用）','沒有 AI 材質圖','分件攤開優先']:
   self.assertIn(text,chair)
 def test_renderer_contract(self):
  js=(ROOT/'docs/mc10/viewer.js').read_text()
  for text in ['ResizeObserver','Raycaster',"'dblclick'",'emissive','makeImages','reportPage',"type:'text/csv;charset=utf-8'",'attributes?.id','localeCompare']:
   self.assertIn(text,js)
if __name__=='__main__':unittest.main()
