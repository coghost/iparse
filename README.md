## iparse

**iparse** is a Python package for parsing HTML to structured data in an easy way with as little code as possible.

It aims to make the process of parsing HTML quick and easy!

iparse highlights:

- mainly code with **YAML**
- only refine raw HTML info with **fewest python code**
- lot's HTML layout changes, only **YAML** will be involved

### Installation

```sh
pip install iparse
```

### A Simple Example

for HTML page: i.e. [lovely xkcd python](https://xkcd.com/353/)

to get the structured data all you need are

- create a class inherit from `IParser`
- write a YAML config file represents all locators

#### create **xkcd_353.py**

`xkcd_353.py` will go through the startup_dir, look for a file named as the snake_case of the ClassName without `suffix:Parser`, so `XkcdParser` will be `xkcd.yaml`

```python
from pathlib import Path
from iparse._parse import IParser, RsvWords

HOME_DIR = Path(__file__).parents[0]


class XkcdParser(IParser):
    def __init__(self, file_name, is_test_mode=False, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', HOME_DIR)
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)


if __name__ == "__main__":
    xkcd = XkcdParser(file_name=HOME_DIR / 'xkcd_python_353.htm')
    xkcd.do_parse()
    print(xkcd.data)
```

#### create a file named **xkcd.yaml**

> you can use any locator that is supported, but [css selector](http://www.java2s.com/Tutorials/HTML_CSS/CSS_Selector/index.htm) is recommended

```yaml
page:
  # css_selector of title: head>title
  title: head>title
  # css_selector: div#footnote
  footnote: div#footnote
  # css_selector: div#licenseText
  license: div#licenseText
```

#### the output parsed data

the parsed data `xkcd.data` is dict, but you can also use it with `xkcd.data_as_yaml/xkcd.data_as_json`

> yaml output

```yaml
page:
  footnote: "xkcd.com is best viewed with Netscape Navigator 4.0 or below on a Pentium\
    \ 3\xB11 emulated in Javascript on an Apple IIGSat a screen resolution of 1024x1.\
    \ Please enable your ad blockers, disable high-heat drying, and remove your devicefrom\
    \ Airplane Mode and set it to Boat Mode. For security reasons, please leave caps\
    \ lock on while browsing."
  license: '


    This work is licensed under a

    Creative Commons Attribution-NonCommercial 2.5 License.


    This means you''re free to copy and share these comics (but not to sell them).
    More details.

    '
  title: 'xkcd: Python'
```

> json output

```json
{
  "page": {
    "footnote": "xkcd.com is best viewed with Netscape Navigator 4.0 or below on a Pentium 3\u00b11 emulated in Javascript on an Apple IIGSat a screen resolution of 1024x1. Please enable your ad blockers, disable high-heat drying, and remove your devicefrom Airplane Mode and set it to Boat Mode. For security reasons, please leave caps lock on while browsing.",
    "license": "\n\nThis work is licensed under a\nCreative Commons Attribution-NonCommercial 2.5 License.\n\nThis means you're free to copy and share these comics (but not to sell them). More details.\n",
    "title": "xkcd: Python"
  }
}
```

### Details

```yaml
# all settings added to __raw, will be kept as it added
__raw:
  site_url: https://xkcd.com/


page:
  # if not _locator supplied will reuse parent soup
  # page has no parent soup, so use default root soup
  title: head>title
  footnote: div#footnote
  license:
    _locator: div#licenseText
    # strip blank with true, but also can specified a str
    _striped: true

top_container:
  # we set a _locator here, all sub-nodes will select within top_container
  _locator: div#topContainer
  top_left:
    # _index:~ means None, so we can use whole list
    _index: ~
    _locator: div#topLeft>ul>li>a
    # if non-reserved key set to ~, means use parent soup, and use its text
    # this is a convenient way to get text
    menu_text: ~
    menu_url:
      # when other attributes exist, no need to add _locator to use its parent soup
      _attr: href
      # if we need some extra work on _attr, goes with two ways
      # 1. `_attr_refine: true` will auto generate => _refine_menu_url_href
      # the rule of auto-generator is _refine_<key_name>_<attr_value>
      # 2. `_attr_refine: _a_valid_method_name`
      _attr_refine: true
  top_right:
    _locator: div#topRight
    masthead:
      # two way to get more than one attributes on a element
      # e.g. image.src/.alt
      # way1: if all src/alt need refine, this will treat attrs as list
      image_1:
        _attr:
          - src
          - alt
        _attr_refine: true
        _locator: &LOGO_IMG span>a>img
      # way2: not all src/alt need refine, this will treat attrs as dict
      image_2:
        _locator: *LOGO_IMG
        src:
          _attr: src
          # only set _attr_refine to src
          # 1. _attr_refine: true => _refine_src_src
          # 2. _attr_refine: _refine_image_1_src to reuse exists method
          _attr_refine: _refine_image_1_src
        alt:
          _attr: alt

      slogan: span#slogan
```

### more

please check the `tests/` for more infomation.
