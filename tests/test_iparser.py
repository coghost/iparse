# -*- coding: utf-8 -*-
__description__ = ''' https://xkcd.com/353/ '''

import os
import sys
from pathlib import Path
import unittest

HOME_DIR = Path(__file__).parents[1]
sys.path.append(str(HOME_DIR))

from iparse import IParser


class XkcdParser(IParser):
    def __init__(self, file_name, is_test_mode=False, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', HOME_DIR / 'tests')
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)

    def _refine_image_1_src(self, raw):
        return self.enrich_url(raw)

    def _refine_image_1_alt(self, raw):
        return raw

    def _refine_menu_url_href(self, raw):
        return self.enrich_url(raw)


class TestXkcdParser(unittest.TestCase):
    def test_01_xkcd353(self):
        xkcd = XkcdParser(
            file_name=HOME_DIR / 'tests/xkcd_python_353.htm',
            is_test_mode=True,
        )
        xkcd.do_parse()
        xkcd.copy_data()
        expected = {
            "page": {
                "title": "xkcd: Python",
                "footnote": "xkcd.com is best viewed with Netscape Navigator 4.0 or below on a Pentium 3\u00b11 emulated in Javascript on an Apple IIGSat a screen resolution of 1024x1. Please enable your ad blockers, disable high-heat drying, and remove your devicefrom Airplane Mode and set it to Boat Mode. For security reasons, please leave caps lock on while browsing.",
                "license": "\n\nThis work is licensed under a\nCreative Commons Attribution-NonCommercial 2.5 License.\n\nThis means you're free to copy and share these comics (but not to sell them). More details.\n",
                "license1": "This work is licensed under a Creative Commons Attribution-NonCommercial 2.5 License . This means you're free to copy and share these comics (but not to sell them). More details .",
                "by_multiple_locators": ["xkcd: Python"],
            },
            "top_container": {
                "top_left": [
                    {"href": "https://xkcd.com/archive", "text": "Archive"},
                    {"href": "http://what-if.xkcd.com", "text": "What If?"},
                    {"href": "http://blag.xkcd.com", "text": "Blag"},
                    {"href": "https://xkcd.com/how-to/", "text": "How To"},
                    {"href": "http://store.xkcd.com/", "text": "Store"},
                    {"href": "https://xkcd.com/about", "text": "About"},
                    {"href": "https://xkcd.com/atom.xml", "text": "Feed"},
                    {"href": "https://xkcd.com/newsletter/", "text": "Email"},
                ],
                "top_right": {
                    "masthead": {
                        "image": {"src": "https://xkcd.com/s/0b7742.png", "alt": "xkcd.com logo"},
                        "slogan": "A webcomic of romance, sarcasm, math, and language.",
                    },
                    "news": {
                        "how_to": "https://xkcd.com/how-to/",
                        "links": [
                            {
                                "href": "https://www.amazon.com/How-Absurd-Scientific-Real-World-Problems/dp/0525537090/",
                                "text": "Amazon",
                            },
                            {
                                "href": "http://links.penguinrandomhouse.com/type/affiliate/isbn/9780525537090/siteID/8001/retailerid/2/trackingcode/PRH5522E62429",
                                "text": "B&N",
                            },
                            {
                                "href": "http://links.penguinrandomhouse.com/type/affiliate/isbn/9780525537090/siteID/8001/retailerid/6/trackingcode/penguinrandom",
                                "text": "IndieBound",
                            },
                            {"href": "https://itunes.apple.com/us/book/how-to/id1451461524?mt=11", "text": "Apple"},
                            {
                                "href": "https://www.audible.com/search?advsearchKeywords=How+To+Randall+Munroe&source_code=COMA0213WS031709&SID=PRHA9A5E24CFB--9780525635680",
                                "text": "Audible",
                            },
                            {
                                "href": "http://links.penguinrandomhouse.com/type/affiliate/isbn/9780525537090/siteID/8001/retailerid/23/trackingcode/PRH3D17167A3B",
                                "text": "Target",
                            },
                        ],
                    },
                },
            },
            "middle_container": {
                "ctitle": "Python",
                "comic_nav": {
                    "nav": [
                        {"href": "https://xkcd.com/1/", "text": "|<", "rel": None, "accesskey": None},
                        {"href": "https://xkcd.com/352/", "text": "< Prev", "rel": ["prev"], "accesskey": ["p"]},
                        {"href": "https://c.xkcd.com/random/comic/", "text": "Random", "rel": None, "accesskey": None},
                        {"href": "https://xkcd.com/354/", "text": "Next >", "rel": ["next"], "accesskey": ["n"]},
                        {"href": "https://xkcd.com/", "text": ">|", "rel": None, "accesskey": None},
                    ]
                },
                "comic": {
                    "src": "//imgs.xkcd.com/comics/python.png",
                    "title": "I wrote 20 short programs in Python yesterday.  It was wonderful.  Perl, I'm leaving you.",
                    "alt": "Python",
                },
                "transcript": "[[ Guy 1 is talking to Guy 2, who is floating in the sky ]]\nGuy 1: You're flying! How?\nGuy 2: Python!\nGuy 2: I learned it last night! Everything is so simple!\nGuy 2: Hello world is just 'print \"Hello, World!\" '\nGuy 1: I dunno... Dynamic typing? Whitespace?\nGuy 2: Come join us! Programming is fun again! It's a whole new world up here!\nGuy 1: But how are you flying?\nGuy 2: I just typed 'import antigravity'\nGuy 1: That's it?\nGuy 2: ...I also sampled everything in the medicine cabinet for comparison.\nGuy 2: But i think this is the python.\n{{ I wrote 20 short programs in Python yesterday.  It was wonderful.  Perl, I'm leaving you. }}",
            },
            "bottom": {
                "comic_map": [
                    {"alt": "Grownups", "coords": "0,0,100,100", "href": "https://xkcd.com/150/"},
                    {"alt": "Circuit Diagram", "coords": "104,0,204,100", "href": "https://xkcd.com/730/"},
                    {"alt": "Angular Momentum", "coords": "208,0,308,100", "href": "https://xkcd.com/162/"},
                    {"alt": "Self-Description", "coords": "312,0,412,100", "href": "https://xkcd.com/688/"},
                    {
                        "alt": "Alternative Energy Revolution",
                        "coords": "416,0,520,100",
                        "href": "https://xkcd.com/556/",
                    },
                ],
                "comic": {"href": "https://xkcd.com/1732/"},
                "feed": [
                    {"href": "https://xkcd.com/rss.xml", "text": "RSS Feed"},
                    {"href": "https://xkcd.com/atom.xml", "text": "Atom Feed"},
                    {"href": "https://xkcd.com/newsletter/", "text": "Email"},
                ],
                "comic_links": [
                    {"href": "http://threewordphrase.com/", "text": "Three Word Phrase"},
                    {"href": "http://www.smbc-comics.com/", "text": "SMBC"},
                    {"href": "http://www.qwantz.com", "text": "Dinosaur Comics"},
                    {"href": "http://oglaf.com/", "text": "Oglaf"},
                    {"href": "http://www.asofterworld.com", "text": "A Softer World"},
                    {"href": "http://buttersafe.com/", "text": "Buttersafe"},
                    {"href": "http://pbfcomics.com/", "text": "Perry Bible Fellowship"},
                    {"href": "http://questionablecontent.net/", "text": "Questionable Content"},
                    {"href": "http://www.buttercupfestival.com/", "text": "Buttercup Festival"},
                    {"href": "http://www.mspaintadventures.com/?s=6&p=001901", "text": "Homestuck"},
                    {"href": "http://www.jspowerhour.com/", "text": "Junior Scientist Power Hour"},
                    {
                        "href": "https://medium.com/civic-tech-thoughts-from-joshdata/so-you-want-to-reform-democracy-7f3b1ef10597",
                        "text": "Tips on technology and government",
                    },
                    {
                        "href": "https://www.nytimes.com/interactive/2017/climate/what-is-climate-change.html",
                        "text": "Climate FAQ",
                    },
                    {"href": "https://twitter.com/KHayhoe", "text": "Katharine Hayhoe"},
                ],
            },
        }

        for k, v in expected.items():
            self.assertEqual(v, xkcd.data[k])


if __name__ == '__main__':
    unittest.main()
