import os
import sys
from pathlib import Path
import unittest

HOME_DIR = Path(__file__).parents[1]
sys.path.append(str(HOME_DIR))

from iparse import IParser


class Xkcd01Parser(IParser):
    def __init__(self, file_name, is_test_mode=False, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', HOME_DIR / 'tests')
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)

    def _refine_menu_url_href(self, raw):
        return self.enrich_url(raw)


class TestXkcd01Parser(unittest.TestCase):
    def test_01_xkcd(self):
        xkcd = Xkcd01Parser(file_name=HOME_DIR / 'tests/xkcd_python_353.htm')
        xkcd.do_parse()
        expected = {
            "page": {
                "footnote": "xkcd.com is best viewed with Netscape Navigator 4.0 or below on a Pentium 3\u00b11 emulated in Javascript on an Apple IIGSat a screen resolution of 1024x1. Please enable your ad blockers, disable high-heat drying, and remove your devicefrom Airplane Mode and set it to Boat Mode. For security reasons, please leave caps lock on while browsing.",
                "license": "This work is licensed under a\nCreative Commons Attribution-NonCommercial 2.5 License.\n\nThis means you're free to copy and share these comics (but not to sell them). More details.",
                "title": "xkcd: Python",
            }
        }
        for k, v in expected.items():
            self.assertEqual(v, xkcd.data[k])


if __name__ == "__main__":
    unittest.main()
