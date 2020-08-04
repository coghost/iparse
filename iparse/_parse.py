# -*- coding: utf-8 -*-
__date__ = '12/06 10:17'
__description__ = '''
'''

import dataclasses
import json
from pathlib import Path
from urllib.parse import urlparse, urljoin
import string

import yaml
import logzero
from logzero import logger as zlog
from stringcase import snakecase, titlecase
import bs4
from bs4 import BeautifulSoup

__all__ = [
    'IParser',
    'IJsonParser',
    'IParserException',
    'RsvWords',
    'yaml_dump',
    'yaml_loader',
]


class IParserException(Exception):
    pass


@dataclasses.dataclass
class RsvWords:
    """ all reserved words """
    attr: str = '_attr'
    attr_refine: str = '_attr_refine'
    children: str = '_children'
    index: str = '_index'
    joiner: str = '_joiner'
    striped: str = '_striped'
    locator: str = '_locator'
    locator_extract: str = '_locator_extract'
    prefix_extract = '_extract'
    prefix_refine = '_refine'


def yaml_loader(file_pth, raw_data=False):
    """
    load yaml to dict
    Args:
        file_pth (str):
        raw_data (bool): if raw_data, will treat file_pth as yaml content

    Returns:
        yaml file as dict
    """
    try:
        if raw_data:
            return yaml.load(file_pth, Loader=yaml.FullLoader)

        file_pth = Path(file_pth)
        if not file_pth.exists():
            raise IParserException('[NON-EXISTS]:{}'.format(file_pth))
        with open(file_pth, 'rb') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        return


def yaml_dump(msg_dict):
    """
    dump dict to yaml
    Args:
        msg_dict ():

    Returns:

    """
    return yaml.dump(msg_dict)


class IParser(object):
    """
    WARN: First of All, any keys of yaml settings in RsvWords will be ignored

    Examples:
        ### 1. init:

        class MetaParser(IParser):
            def __init__(self, file_name='', is_test_mode=False, **kwargs):
                kwargs.startup_dir = kwargs.get('startup_dir', SETTINGS_DIR)
                super().__init__(file_name, is_test_mode=is_test_mode)

        ### 2. customize:

        kwargs['log_level'] = kwargs.get('log_level', 20)
        kwargs['basic_yaml'] = kwargs.get('basic_yaml', DIR / 'base.yaml')
    """

    def __init__(self, file_name='', *args, **kwargs):
        """

        Args:
            file_name ():
            *args ():
            **kwargs (): file_name
        """
        self.file_name = file_name
        self.raw_data = kwargs.get('raw_data', '')
        self.mapper = {}
        self.soup = None
        self.site_name = titlecase(self.__class__.__name__.replace('Parser', ''))
        self.snake_site_name = snakecase(self.__class__.__name__.replace('Parser', ''))

        self.log_level = kwargs.get('log_level', 10)
        # convert startup_dir to PurePath
        self.startup_dir = Path(str(kwargs.get('startup_dir', '/tmp')))
        # a basic yaml is shared configs among all yaml files
        self.basic_yaml = kwargs.get('basic_yaml', '')
        # site yaml file is where all site's selector behold
        self.startup_yaml = kwargs.get('startup_yaml', self.snake_site_name)
        # if is_test_mode, will raise exceptions instead of log
        self.is_test_mode = kwargs.get('is_test_mode', False)
        self.test_keys = kwargs.get('test_keys', [])
        # bs4 basic configs
        self.encoding = kwargs.get('encoding', '')
        self.features = kwargs.get('features', 'lxml')
        self.reserved_yaml_keys = kwargs.get('reserved_yaml_keys', [])
        self.elems_default_index = kwargs.get('elems_default_index', 0)

        # where our parsed data behold
        self._data = {}
        self._spawn()

    def __str__(self):
        _base = '{}\n'.format(self.__class__.__name__)
        for key, val in self.__dict__.items():
            if isinstance(val, bs4.Tag):
                continue
            _base += '{:>16}: {}\n'.format(key, val)
        return _base

    def _spawn(self):
        # init log level
        self.pre_init()
        # load basic mapper
        self.load_mapper()
        self.init_soup()
        self.post_init()

    def pre_init(self):
        logzero.loglevel(self.log_level)
        self.reserved_yaml_keys += dataclasses.astuple(RsvWords())

    def post_init(self):
        _test_keys = self.mapper.get('__raw', {}).pop('test_keys', []) or []
        self.test_keys += _test_keys

    def load_mapper(self):
        if self.basic_yaml:
            self.mapper = yaml_loader(str(self.startup_dir / self.basic_yaml))
        self.customize_with_file(self.startup_yaml)

    def customize_with_file(self, file_name):
        """
        typical usage:

        1. init site yaml file with auto-gen snake name
        2. overwrite startup snake name yaml

        Args:
            file_name (str): using which file as startup yaml

        """
        _custom = self._load_yaml_config(file_name)
        for _key in _custom.keys():
            if isinstance(_custom[_key], dict):
                self.mapper[_key] = dict(self.mapper.get(_key, {}), **_custom.get(_key, {}))
            else:
                self.mapper[_key] = _custom[_key]

    def _load_yaml_config(self, file_name):
        _site_startup_yaml = self.startup_dir / '{}.yaml'.format(file_name)
        if _site_startup_yaml.exists():
            return yaml_loader(_site_startup_yaml)
        raise IParserException('site startup yaml ({}) not exists'.format(_site_startup_yaml))

    def init_soup(self, raw_data=''):
        """
        init soup for parser, if raw_data supplied, will refresh self.soup

            - fail over with 'html.parser'

        Args:
            raw_data (): if you want refresh soup, can call this method with raw_data
        """
        if raw_data:
            self.raw_data = raw_data
        if not self.raw_data:
            with open(self.file_name, 'rb') as fp:
                self.raw_data = fp.read()

        params = dict(
            features=self.features,
        )
        if self.encoding:
            params['from_encoding'] = self.encoding
        try:
            self.soup = BeautifulSoup(self.raw_data, **params)
        except bs4.FeatureNotFound:
            params['features'] = 'html.parser'
            self.soup = BeautifulSoup(self.raw_data, **params)

    @property
    def data(self):
        return self._data

    @property
    def data_as_json(self):
        return json.dumps(self._data, indent=2, sort_keys=True)

    @property
    def data_as_yaml(self):
        return yaml_dump(self._data)

    @staticmethod
    def shift(dat):
        if isinstance(dat, dict):
            return yaml_dump(dat)
        return yaml_loader(dat, raw_data=True)

    def do_parse(self):
        for dom_key, dom_config in self.mapper.items():
            if dom_key.startswith('__'):
                continue

            if dom_key in self.reserved_yaml_keys:
                zlog.error('[RESERVED-KEYS] ({})'.format(dom_key))
                continue

            if not isinstance(dom_config, dict):
                zlog.error('[PLAIN-TYPE] {}:{}, please move inside page'.format(dom_key, dom_config))
                continue

            if all([self.is_test_mode, self.test_keys, dom_key not in self.test_keys]):
                zlog.debug('[SKIPPED-KEYS] ({})'.format(dom_key))
                continue

            self._parse_dom(dom_key, dom_config, self.soup, self._data)

    """ operation on DOMs """

    def dom_with_sub_nodes(self, config):
        """ if all key startswith _, means all reserved keys, leaf node """
        sub_node = []
        if isinstance(config, dict):
            sub_node = [k for k, _ in config.items() if not k.startswith('_')]
        return sub_node

    def _parse_dom(self, key, config, nodes, dat):
        """
        parse html dom with recursion of `_parse_dom/_parse_dom_nodes`

        two end conditions:
            1. config is str
            2. no child in config dom nodes
            3. nodes not exist

        Args:
            key (str):
            config (str/dict/None):
            nodes (Tag/list):
            dat (dict):
        """
        if not self.dom_with_sub_nodes(config):
            dat[key] = self._get_node_attrs(key, config, nodes)
            return

        nodes = self._get_node_elems(key, config, nodes)
        # nodes not exists
        if not nodes:
            zlog.debug("[NON-NODES] ('{}': {})".format(key, config))
            return

        if isinstance(nodes, list):
            dat.setdefault(key, [])
            for node in nodes:
                sub_dat = {}
                self._parse_dom_nodes(config, node, sub_dat)
                dat[key].append(sub_dat)
        else:
            dat.setdefault(key, {})
            self._parse_dom_nodes(config, nodes, dat[key])

    def _parse_dom_nodes(self, children, node, dat):
        for _key, _config in children.items():
            if _key.startswith('_'):
                continue
            self._parse_dom(_key, _config, node, dat)

    """ how we find and parse attributes """

    def _get_node_elems(self, key, config, node=None, **kwargs):
        """
        e.g. example for all kinds of key:config

        ```yaml

        top_container:
          _locator: div#topContainer
          top_left:
            _locator: div#topLeft>ul>li>a   # gn2
            menu_text: ~ # gn1
            menu_url:
              # gn3.1
              _locator_extract: true    # gn4.2
            menu_extract_str:
              _locator_extract: _extract_menu_str    # gn4.1
            wrong_usage:
              _locator: ''  # gn3.2
            menu_index1:
              _index: ~  # gn5.1
            menu_index2:
              _index: 0  # gn5.2
            menu_index3:
              # gn5.3
              _index:
                - 0
                - -2
            menu_index4:
              _index: a  # gn5.4

        ```

        Args:
            key (str):
            config (str/dict):
            node (None/BS4):
            **kwargs():

        Returns:
            bs4.Tag/list[bs4.Tag]
        """
        try:
            return self.get_node_elems(key, config, node, **kwargs)
        except Exception as e:
            if self.is_test_mode:
                raise IParserException(e)
            else:
                zlog.exception(e)

    def select_soup_node_elems(self, node, key, multiple=True):
        elems = getattr(node, 'select')(key)
        if multiple:
            return elems
        return elems[0] if elems else elems

    def get_node_elems(self, key, config, node=None, **kwargs):
        node = node or self.soup

        # gn1. first of all: if config is None, means use current node
        if config is None:
            return node

        if not config:
            raise Exception(f"[Err] _locator({key}:{config})'s value can not be empty")

        # gn2. simple str, select and return
        if isinstance(config, str):
            elems = self.select_soup_node_elems(node, config, multiple=False)
            return elems

        # gn3. config is dict
        # gn3.1 _locator is None, use current node
        _locator = config.get(RsvWords.locator)
        if _locator is None:
            return node

        # gn3.2 in case if you mistakenly add `_locator: ''` or things like this
        if not _locator:
            zlog.warning('[TYPO] please use `_locator: ~` or `remove _locator` instead of ({},{},{})'.format(
                key, config, _locator
            ))
            return node

        elems = self.select_soup_node_elems(node, _locator)
        # gn4. with _locator_extract
        _locator_extract = config.get(RsvWords.locator_extract)
        elems = self.__extract_elems(key, _locator_extract, elems)
        if not elems:
            return None

        # gn5. get all or just specified
        elems = self.__filter_specified_elems(elems, config)
        return elems

    def __extract_elems(self, key, _locator_extract, elems):
        # TODO: find if _extract need list structure
        # gn4.1 _locator_extract is str, just use it.
        if _locator_extract is True:
            # gn4.2 if is true => auto-generate _extract_<key_name>
            _locator_extract = '{}_{}'.format(RsvWords.prefix_extract, key)
        if _locator_extract:
            # gn4.1/4.2: str/bool
            elems = getattr(self, _locator_extract)(elems)

        return elems

    def __filter_specified_elems(self, elems, config):
        # index: None = all, int = only one, list = range
        index = config.get(RsvWords.index, self.elems_default_index)
        # gn5.1 `index: ~`
        if index is None:
            return elems
        # gn5.2 `index: <int>`
        if isinstance(index, int):
            index = min(index, len(elems) - 1)
            return elems[index]
        # gn5.3 `index: <list>`
        if isinstance(index, list):
            if len(index) == 1:
                return elems[index[0]:]
            else:
                return elems[index[0]:index[-1]]

        # gn5.4 `index: non-previous value`
        if self.is_test_mode:
            raise IParserException('error type of {} index({})'.format(config, index))
        else:
            zlog.exception('[ERROR-TYPE] type of {} index({})'.format(config, index))
        return elems

    def _get_nodes_attrs(self, key, config, node=None, **kwargs):
        return [
            self._get_node_attrs(key, config, _node) for _node in node
        ]

    def _get_node_attrs(self, key, config, node=None, **kwargs):
        """
        1. get node's all elems
        2. get each elem's attrs

        Args:
            key (str):
            config (str/dict):
            node ():
            **kwargs ():
        Returns:
            str/list
        """
        node = node or self.soup

        # in case got node list
        if isinstance(node, list):
            zlog.warning('[MULTIPLE-NODE]type of node is list: {}{}'.format(key, config))
            return ''

        elems = self._get_node_elems(key, config, node)
        if not elems:
            zlog.debug('[NON-ELEMS]: {}/{} find nothing'.format(key, config))
            return ''

        if not isinstance(elems, list):
            return self._get_elem_attrs(elems, key, config)

        return [
            self._get_elem_attrs(elem, key, config) for elem in elems
        ]

    def _get_elem_attrs(self, elem, key, config):
        """ get elem's attributes

        e.g. example for all kinds of key:config

        ```yaml

        top_container:
          _locator: div#topContainer
          top_left:
            _locator: div#topLeft>ul>li>a   # ga2
            menu_text: ~ # ga1
            menu_1:
              # gn3.1.1
              _attr:
                - src
                - alt
            menu_2:
              _attr: href   # gn3.1.2
            menu_3:
              _joiner: ','   # gn3.2
              _striped: true/false
            menu_4:
              # gn3.3: no _attr, no _joiner
              _striped: true/false
              ...
        ```
        """
        # 1.1 non-elem
        if not elem:
            return ''
        # 1.2 elem not bs4.Tag
        if not isinstance(elem, bs4.Tag):
            return elem

        # ga1. config is None, just return
        if config is None:
            return elem.text

        # ga2. config is simple str selector, just return
        if isinstance(config, str):
            return elem.text

        # ga3. config is dict
        _attrs = config.get(RsvWords.attr)
        _joiner = config.get(RsvWords.joiner, '')
        _striped = config.get(RsvWords.striped, False)

        # ga3.1 parse attr/joiner/text
        # TODO: add examples from here
        if _attrs:
            # ga3.1 _attr is the prime one
            raw = self._get_prime_attr(elem, _attrs)
        elif _joiner:
            # ga3.2 parse _joiner
            raw = elem.get_text(_joiner, strip=_striped) or ''
        else:
            # ga3.3 parse text
            raw = self.get_striped_text(elem, _striped)

        # ga4. refine attribute
        return self.__refine_attr__(key, config, _attrs, raw)

    def _get_prime_attr(self, elem, attr):
        # ga3.1.1 attr is list
        if isinstance(attr, list):
            return {
                _attr: elem.get(_attr, '') for _attr in attr
            }

        # ga3.1.2 attr is str
        return elem.get(attr)

    def get_striped_text(self, elem, _striped=False, keep_original=False):
        raw = elem if keep_original else elem.text

        if _striped is True:
            return raw.strip()
        if isinstance(_striped, str):
            for x in _striped:
                raw = raw.replace(x, '')
            return raw

        return raw

    def __refine_attr__(self, key, config, _attrs, raw):
        """
        ga4.1 non refine
        ga4.2 if attr_refine is str, just use it
        ga4.3 else auto parse it

        when _attr is `ga3.1.1`
        image_1:
            _attr:
              - src
              - alt
            _attr_refine: true
            _locator: span>a>img

        image_2:
            _locator: span>a>img
            src:
              _attr: src
              _attr_refine: _refine_image_1_src
            alt:
              _attr: alt
        """
        # ga4.1 non-refine
        _attr_refine = config.get(RsvWords.attr_refine)
        if not _attr_refine:
            return raw

        # ga4.2 raw is dict, means _attr is `ga3.1.1`
        if isinstance(raw, dict):
            if _attr_refine is True:
                _attr_refine = '{}_{}'.format(RsvWords.prefix_refine, key)
            return {
                k: getattr(self, '{}_{}'.format(_attr_refine, k))(v) for k, v in raw.items()
            }

        # ga4.3 raw is normal str
        if _attr_refine is True:
            _fmt = '{}_{}'
            if isinstance(_attrs, str):
                _fmt = '{}_{}_{}'
            _attr_refine = _fmt.format(RsvWords.prefix_refine, key, _attrs)
            # only keep characters allowed by python function names
            _attr_refine = self.keep_allowed_chars(_attr_refine, replace_with='')
        raw = getattr(self, _attr_refine)(raw)
        return raw

    """ staticmethod """

    @staticmethod
    def last_non_empty_info(info, sep='\n', index=-1):
        """
        split info with sep, and return specified index's value

        trick: if index is None, will return all value

        Args:
            info (str):
            sep (str):
            index (int/None):

        Returns:
            specified index value/all value list
        """
        if not info:
            return ''
        if index is None:
            return [x for x in info.split(sep)]
        info = [x for x in info.split(sep) if x.strip()]
        return info[index].strip() if info else ''

    @staticmethod
    def keep_allowed_chars(src, custom='_', replace_with=''):
        chars_allowed = string.ascii_letters + string.digits + custom
        dst = ''.join([x if x in chars_allowed else replace_with for x in src])
        return dst

    @staticmethod
    def char_to_num(src, chars_allowed='0123456789', custom=''):
        """ simple number only filter

        Args:
            src (str): orig string
            chars_allowed (str): remained string
            custom (str): extra custom chars remained

        Returns:
            all chars in chars_allowed
        """
        if custom:
            chars_allowed += custom
        n = ''.join(list([c for c in src if c in chars_allowed]))
        return n

    """ all following methods are used for enrich parsed results """

    def enrich_url(self, info, domain=''):
        if urlparse(info).scheme:
            return info
        domain = domain or self.mapper['__raw']['site_url']
        return urljoin(domain, info)

    def enrich_dot_k(self, info, custom='.'):
        k = 'k'
        unit = 1000 if k in info else 1
        info = self.char_to_num(info.lower(), custom=custom)
        if not info:
            return 0
        return float(info) * unit

    def enrich_k(self, info):
        return self.enrich_dot_k(info, custom='')

    def enrich_dot_k_int(self, info, custom='.'):
        return int(self.enrich_dot_k(info, custom))

    def enrich_k_int(self, info):
        return int(self.enrich_dot_k(info, custom=''))


class IJsonParser(IParser):
    def __init__(self, file_name='', *args, **kwargs):
        kwargs['elems_default_index'] = kwargs.get('elems_default_index', None)
        self.cascade_sep = kwargs.pop('cascade_sep', '.')
        super().__init__(file_name, *args, **kwargs)

    def init_soup(self, raw_data=''):
        """ a valid json should be a dict or list """
        if raw_data:
            self.raw_data = raw_data
        if not self.raw_data:
            with open(self.file_name, 'rb') as fp:
                self.raw_data = fp.read()

        self.soup = json.loads(self.raw_data)
        # T1: dict
        if isinstance(self.soup, dict):
            return

        if not isinstance(self.soup, list):
            raise Exception(f'Error loading SERP: {self.file_name}')
        # T2: list
        self.soup = [x for x in self.soup if x]

    def select_soup_node_elems(self, root, locator, multiple=True):
        """
        in case some file's keys goes with `self.cascade_sep`, so we need go through the whole locator
        e.g.:
            root = A
            locator = `features./job_category.values`

        steps of find locator's elem:
            1. A.get(features./job_category.values)
            2. A.get(features).get(/job_category.values)
            3. A.get(features).get(/job_category).get(values)
            4. ...
        """
        # locator exists, that's it
        if locator in root:
            return root.get(locator, '')

        # e.g.: `features./job_category.values`
        cascade_keys = locator.split(self.cascade_sep)
        elem_container = root
        for i in range(len(cascade_keys)):
            head, tail = cascade_keys[i], self.cascade_sep.join(cascade_keys[i + 1:])
            elem_container = elem_container.get(head, {})
            elem = elem_container.get(tail)
            if elem:
                return elem

    def _get_elem_attrs(self, elem, key, config):
        if not elem:
            return ''

        if not isinstance(config, dict):
            return elem

        _attrs = config.get(RsvWords.attr)
        _striped = config.get(RsvWords.striped, False)

        if _attrs:
            raw = self._get_prime_attr(elem, _attrs)
        else:
            raw = self.get_striped_text(elem, _striped, keep_original=True)

        return self.__refine_attr__(key, config, '', raw)

    def __refine_attr__(self, key, config, _attrs, raw):
        _attr_refine = config.get(RsvWords.attr_refine)
        if not _attr_refine:
            return raw

        if _attr_refine is True:
            _fmt = '{}_{}'
            _attr_refine = _fmt.format(RsvWords.prefix_refine, key)
            # only keep characters allowed by python function names
            _attr_refine = self.keep_allowed_chars(_attr_refine, replace_with='')

        return getattr(self, _attr_refine)(raw)
