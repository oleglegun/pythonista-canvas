import sys
import os
print(sys.path)
abspath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

sys.path.insert(0, abspath)
print(sys.path)
#sys.exit()
import unittest
import helpers


class TestHelpers(unittest.TestCase):
    def test_rgb_to_hsl(self):
        test_data = [
            [(0, 0, 0), (0, 0, 0)],
            [(255, 255, 255), (0, 0, 1)],
#            [(34, 230, 103), (0, 0, 0)]
            
            ]
        
        for test in test_data:
            rgb = test[0]
            hsl = test[1]
            self.assertEqual(helpers.rgb_to_hsl(*rgb), hsl)
    def test_hsl_to_rgb(self):
        test_data = [
            [(0, 0, 0), (0, 0, 0)],
            [(0.5, 0.5, 0.5), (191.25, 64.8125, 63.75)]
            ]
        for test in test_data:
            hsl = test[0]
            rgb = test[1]
            self.assertEqual(helpers.hsl_to_rgb(*hsl), rgb)
