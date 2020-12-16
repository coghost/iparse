# -*- coding: utf-8 -*-
__description__ = ''' https://xkcd.com/353/ '''

from pathlib import Path
from iparse import IParser

HOME_DIR = Path(__file__).parents[1]


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


if __name__ == '__main__':
    xkcd = XkcdParser(
        file_name=HOME_DIR / 'tests/xkcd_python_353.htm',
        is_test_mode=True,
    )
    xkcd.do_parse()
    print(xkcd.data_as_yaml)
