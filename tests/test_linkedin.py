# -*- coding: utf-8 -*-
from pathlib import Path
from iparse import IParser

HOME_DIR = Path(__file__).parents[1]
EN_DASH = '\u2013'


class LinkedinParser(IParser):
    def __init__(self, file_name, is_test_mode=False, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', HOME_DIR / 'tests')
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)

    def _refine_recommendations(self, raw):
        return int(self.last_non_empty_info(raw, ' ', 0))

    def _refine_duration(self, raw):
        return ''.join(raw).replace(EN_DASH, '-').replace(' ', '')

    def _refine_exp_duration(self, raw):
        raw = [x.replace(EN_DASH, '').strip() for x in raw.split(',')]
        raw = [x for x in raw if x]
        return ','.join(raw)

    def _refine_status_data_section(self, raw):
        return 'current position' if 'current' in raw.lower() else 'post position'


def run():
    lkn = LinkedinParser(
        file_name=HOME_DIR / 'tests/linkedin.html',
        is_test_mode=True,
    )

    lkn.do_parse()
    print(lkn.data_as_yaml)


if __name__ == '__main__':
    run()
