# -*- coding: utf-8 -*-
from pathlib import Path
from iparse import IJsonParser

HOME_DIR = Path(__file__).parents[1]


class ListDemoParser(IJsonParser):
    def __init__(self, file_name, is_test_mode=False, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', HOME_DIR / 'tests')
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)

    def _refine_size(self, raw):
        return raw.replace('人', '')

    def _refine_industry(self, raw):
        return raw.split(',')


class DictDemoParser(IJsonParser):
    def __init__(self, file_name, is_test_mode=False, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', HOME_DIR / 'tests')
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)


def run_ddp():
    ddp = DictDemoParser(
        file_name=HOME_DIR / 'tests/dict_demo.json',
        is_test_mode=True,
    )
    ddp.do_parse()
    print(ddp.data_as_json)


def run_ldp():
    ldp = ListDemoParser(
        file_name=HOME_DIR / 'tests/list_demo.json',
        is_test_mode=True,
    )
    ldp.do_parse()
    print(ldp.data_as_json)


if __name__ == '__main__':
    run_ddp()
    run_ldp()
