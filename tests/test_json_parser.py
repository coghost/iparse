# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import unittest

HOME_DIR = Path(__file__).parents[1]
sys.path.append(str(HOME_DIR))

from iparse import IJsonParser


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


class TestJsonParser(unittest.TestCase):
    def test_01_run_ddp(self):
        ddp = DictDemoParser(
            file_name=HOME_DIR / 'tests/dict_demo.json',
            is_test_mode=True,
        )
        ddp.do_parse()

        expected = {
            "glossary": {
                "gloss_entry": {
                    "abbrev": "ISO 8879:1986",
                    "def_para": "A meta-markup language, used to create markup languages such as DocBook.",
                    "gid": "SGML",
                    "see_also": ["GML", "XML"],
                    "sort_as": "SGML",
                },
                "gloss_title": "S",
                "title": "example glossary",
            },
            "maps_data": {
                "destination": [
                    "Washington, DC, USA",
                    "Philadelphia, PA, USA",
                    "Santa Barbara, CA, USA",
                    "Miami, FL, USA",
                    "Austin, TX, USA",
                    "Napa County, CA, USA",
                ],
                "rows": [
                    {
                        "elements": [
                            {"distance": "227 mi", "duration": "3 hours 54 mins", "status": "OK"},
                            {"distance": "94.6 mi", "duration": "1 hour 44 mins", "status": "OK"},
                            {"distance": "2,878 mi", "duration": "1 day 18 hours", "status": "OK"},
                            {"distance": "1,286 mi", "duration": "18 hours 43 mins", "status": "OK"},
                            {"distance": "1,742 mi", "duration": "1 day 2 hours", "status": "OK"},
                            {"distance": "2,871 mi", "duration": "1 day 18 hours", "status": "OK"},
                        ]
                    }
                ],
            },
        }
        for k, v in expected.items():
            self.assertEqual(v, ddp.data[k])

    def test_02_run_ldp(self):
        ldp = ListDemoParser(
            file_name=HOME_DIR / 'tests/list_demo.json',
            is_test_mode=True,
        )
        ldp.do_parse()

        expected = {
            "jobs": [
                {
                    "city": "鞍山",
                    "company": {
                        "name": "辽宁福鞍燃气轮机有限公司",
                        "size": "100-299",
                        "type": "上市公司",
                        "url": "https://company.zhaopin.com/CZ581421280.htm",
                    },
                    "education": {"name": "本科"},
                    "experience": "5-10年",
                    "external_id": "CC581421280J00263439811-1596451792253",
                    "industry": ["129900", "300000"],
                    "job_type": "机械设计/制造/维修",
                    "listing_date": "2020-08-03 00:51:45",
                    "number": "CC581421280J00263439811",
                    "salary": "6K-12K",
                    "staff": {"hr_job": "人力专员", "name": "HR"},
                    "title": "机械工艺工程师",
                    "url": "https://jobs.zhaopin.com/CC581421280J00263439811.htm",
                    "vip_level": 1002,
                    "welfare": ["五险一金", "餐补", "健身俱乐部", "补充医疗保险", "周末双休"],
                },
                {
                    "city": "鞍山",
                    "company": {
                        "name": "辽宁超鹏服饰有限公司",
                        "size": "100-299",
                        "type": "民营",
                        "url": "http://special.zhaopin.com/pagepublish/36134381/index.html",
                    },
                    "education": {"name": "本科"},
                    "experience": "3-5年",
                    "external_id": "CC361343813J00257246209-1596451792253",
                    "industry": ["121100", "170500"],
                    "job_type": "销售业务",
                    "listing_date": "2020-08-03 00:51:39",
                    "number": "CC361343813J00257246209",
                    "salary": "3K-6K",
                    "staff": {"hr_job": "经理", "name": "张鹏"},
                    "title": "外贸业务员",
                    "url": "https://jobs.zhaopin.com/CC361343813J00257246209.htm",
                    "vip_level": 1002,
                    "welfare": ["五险一金", "包住", "带薪年假", "健身俱乐部", "项目奖金"],
                },
                {
                    "city": "鞍山",
                    "company": {
                        "name": "鞍山万正裕盈网络科技有限公司",
                        "size": "20-99",
                        "type": "民营",
                        "url": "https://company.zhaopin.com/CZ605762330.htm",
                    },
                    "education": {"name": "初中及以下"},
                    "experience": "不限",
                    "external_id": "CC605762330J00268249613-1596451792253",
                    "industry": ["160400"],
                    "job_type": "销售业务",
                    "listing_date": "2020-08-03 00:51:59",
                    "number": "CC605762330J00268249613",
                    "salary": "6K-8K",
                    "staff": {"hr_job": "总经理", "name": "李先生"},
                    "title": "市场销售专员",
                    "url": "https://jobs.zhaopin.com/CC605762330J00268249613.htm",
                    "vip_level": 1002,
                    "welfare": ["五险一金", "绩效奖金", "弹性工作", "通讯补助", "补充医疗保险"],
                },
                {
                    "city": "鞍山",
                    "company": {
                        "name": "辽宁希思腾科信息技术有限公司",
                        "size": "20-99",
                        "type": "不限",
                        "url": "https://company.zhaopin.com/CZ262638280.htm",
                    },
                    "education": {"name": "中专/中技"},
                    "experience": "1-3年",
                    "external_id": "CZ262638280J00047303712-1596451792253",
                    "industry": ["160400"],
                    "job_type": "技工/操作工",
                    "listing_date": "2020-08-03 00:51:53",
                    "number": "CZ262638280J00047303712",
                    "salary": "2K-3K",
                    "staff": {"hr_job": "人资企管部经理", "name": "冯先生"},
                    "title": "组装装配",
                    "url": "https://jobs.zhaopin.com/CZ262638280J00047303712.htm",
                    "vip_level": 1002,
                    "welfare": ["周末双休", "五险一金", "餐补", "免费班车", "带薪年假"],
                },
                {
                    "city": "鞍山",
                    "company": {
                        "name": "辽宁希思腾科信息技术有限公司",
                        "size": "20-99",
                        "type": "不限",
                        "url": "https://company.zhaopin.com/CZ262638280.htm",
                    },
                    "education": {"name": "本科"},
                    "experience": "3-5年",
                    "external_id": "CC262638281J00216984312-1596451792253",
                    "industry": ["160400"],
                    "job_type": "客服/售前/售后技术支持",
                    "listing_date": "2020-08-03 00:51:53",
                    "number": "CC262638281J00216984312",
                    "salary": "4K-6K",
                    "staff": {"hr_job": "人资企管部经理", "name": "冯先生"},
                    "title": "结构工程师/机械工程师",
                    "url": "https://jobs.zhaopin.com/CC262638281J00216984312.htm",
                    "vip_level": 1002,
                    "welfare": ["五险一金", "加班补助", "交通补助", "餐补", "带薪年假"],
                },
                {
                    "city": "鞍山",
                    "company": {
                        "name": "鞍山金地置业开发有限公司",
                        "size": "20-99",
                        "type": "民营",
                        "url": "https://company.zhaopin.com/CZ380577580.htm",
                    },
                    "education": {"name": "中专/中技"},
                    "experience": "5-10年",
                    "external_id": "CC380577589J00405435007-1596451792253",
                    "industry": ["140000"],
                    "job_type": "交通运输服务",
                    "listing_date": "2020-08-03 00:50:34",
                    "number": "CC380577589J00405435007",
                    "salary": "2K-4K",
                    "staff": {"hr_job": "文员", "name": "芦媛"},
                    "title": "总裁司机",
                    "url": "https://jobs.zhaopin.com/CC380577589J00405435007.htm",
                    "vip_level": 1002,
                    "welfare": ["年终分红", "包吃", "免费停车", "节日福利"],
                },
            ]
        }

        self.assertIn('jobs', expected)
        jobs = expected['jobs']
        self.assertListEqual(jobs, ldp.data['jobs'])


if __name__ == '__main__':
    unittest.main()
