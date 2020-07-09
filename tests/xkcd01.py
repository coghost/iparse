from pathlib import Path
from iparse._parse import IParser, RsvWords

HOME_DIR = Path(__file__).parents[0]


class Xkcd01Parser(IParser):
    def __init__(self, file_name, is_test_mode=False, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', HOME_DIR)
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)

    def _refine_menu_url_href(self, raw):
        return self.enrich_url(raw)


if __name__ == "__main__":
    xkcd = Xkcd01Parser(file_name=HOME_DIR / 'xkcd_python_353.htm')
    xkcd.do_parse()
    print(xkcd.data_as_yaml)
