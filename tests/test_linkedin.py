# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import logzero
import unittest

HOME_DIR = Path(__file__).parents[1]
sys.path.append(str(HOME_DIR))

from iparse import IParser

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


class TestLinkedinParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self) -> None:
        logzero.loglevel(10)

    def test_01_run(self):
        lkn = LinkedinParser(
            file_name=HOME_DIR / 'tests/linkedin.html',
            is_test_mode=True,
        )
        logzero.loglevel(20)
        lkn.do_parse()
        expected = {
            "activities": [
                {
                    "header": "Articles by Barack",
                    "posts": [
                        {
                            "author": {
                                "link_page": "https://www.linkedin.com/in/barackobama?trk=public_profile_article_actor-name",
                                "link_text": "Barack Obama",
                            },
                            "link": "https://www.linkedin.com/pulse/20130122172253-11932467--our-journey-is-not-complete?articleId=10721#comments-10721&trk=public_profile_article_view",
                            "pub_date": "January 22, 2013",
                        },
                        {
                            "author": {
                                "link_page": "https://www.linkedin.com/in/barackobama?trk=public_profile_article_actor-name",
                                "link_text": "Barack Obama",
                            },
                            "link": "https://www.linkedin.com/pulse/20130118175701-11932467-welcome-to-organizing-for-action?articleId=10138#comments-10138&trk=public_profile_article_view",
                            "pub_date": "January 18, 2013",
                        },
                        {
                            "author": {
                                "link_page": "https://www.linkedin.com/in/barackobama?trk=public_profile_article_actor-name",
                                "link_text": "Barack Obama",
                            },
                            "link": "https://www.linkedin.com/pulse/20130107171535-11932467-restoring-fairness-to-our-tax-system?articleId=9585#comments-9585&trk=public_profile_article_view",
                            "pub_date": "January 7, 2013",
                        },
                    ],
                }
            ],
            "education": [
                {
                    "details": "Activities and Societies: Editor, Harvard Law Review, 1990",
                    "duration": "1988,1991",
                    "school": {
                        "link_page": "https://www.linkedin.com/school/harvard-university/?trk=public_profile_school_result-card_full-click",
                        "link_text": "Harvard University",
                    },
                    "subtitle": "Juris DoctorLaw",
                    "title": "Harvard University",
                },
                {
                    "details": "",
                    "duration": "1981,1983",
                    "school": {
                        "link_page": "https://www.linkedin.com/school/columbia-university/?trk=public_profile_school_result-card_full-click",
                        "link_text": "Columbia University in the City of New York",
                    },
                    "subtitle": "Bachelor of ArtsPolitical Science, concentration in International Relations",
                    "title": "Columbia University in the City of New York",
                },
                {
                    "details": "",
                    "duration": "1979,1981",
                    "school": {
                        "link_page": "https://www.linkedin.com/school/occidental-college/?trk=public_profile_school_result-card_full-click",
                        "link_text": "Occidental College",
                    },
                    "subtitle": "Political Science",
                    "title": "Occidental College",
                },
            ],
            "experience": {
                "positions": [
                    {
                        "experience": {
                            "description": "I served as the 44th President of the United States of America.",
                            "duration": "Jan 2009,Jan 2017,8 years 1 month",
                            "location": "",
                            "subtitle": "",
                            "title": "President",
                        },
                        "status": "post position",
                    },
                    {
                        "company": {
                            "link": "https://www.linkedin.com/company/united-states-senate?trk=public_profile_experience-item_result-card_image-click",
                            "name": "US Senate (IL-D)",
                        },
                        "experience": {
                            "description": "In the U.S. Senate, I sought to focus on tackling the challenges of a globalized, 21st century world with fresh thinking and a politics that no longer settles for the lowest common denominator.",
                            "duration": "Jan 2005,Nov 2008,3 years 11 months",
                            "location": "",
                            "subtitle": "US Senate (IL-D)",
                            "title": "US Senator",
                        },
                        "status": "post position",
                    },
                    {
                        "experience": {
                            "description": "Proudly representing the 13th District on Chicago's south side.",
                            "duration": "1997,2004,7 years",
                            "location": "",
                            "subtitle": "",
                            "title": "State Senator",
                        },
                        "status": "post position",
                    },
                    {
                        "company": {
                            "link": "https://www.linkedin.com/company/university-of-chicago-law-school?trk=public_profile_experience-item_result-card_image-click",
                            "name": "University of Chicago Law School",
                        },
                        "experience": {
                            "description": "",
                            "duration": "1993,2004,11 years",
                            "location": "",
                            "subtitle": "University of Chicago Law School",
                            "title": "Senior Lecturer in Law",
                        },
                        "status": "post position",
                    },
                ]
            },
            "page": {
                "people": "Barack Obama",
                "title": "Barack Obama - Washington D.C. Metro Area | Professional Profile | LinkedIn",
            },
            "peopleRelated": {
                "browsemap": {
                    "people": [
                        {
                            "card": {
                                "link_page": "https://ca.linkedin.com/in/justintrudeau?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Justin Trudeau",
                            },
                            "subtitle": "Prime Minister of Canada | Premier ministre du Canada",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/owinfrey?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Oprah Winfrey",
                            },
                            "subtitle": "CEO, Producer, Publisher, Actress and Innovator",
                        },
                        {
                            "card": {
                                "link_page": "https://in.linkedin.com/in/narendramodi?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Narendra Modi",
                            },
                            "subtitle": "Prime Minister of India",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/marva-king-a456a7b?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Marva King",
                            },
                            "subtitle": "CEO at Marvalous Works Entertainment",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/rksolidnyc?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Rebecca Kennedy",
                            },
                            "subtitle": "Master Instructor at Peloton",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/anjalisud?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Anjali Sud",
                            },
                            "subtitle": "CEO, Vimeo",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/daniel-ek-1b52093a?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Daniel Ek",
                            },
                            "subtitle": "CEO and Founder at Spotify",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/satyanadella?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Satya Nadella",
                            },
                            "subtitle": "CEO at Microsoft",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/jessica-alba?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Jessica Alba",
                            },
                            "subtitle": "Founder of The Honest Company",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/ajaybanga?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Ajay Banga",
                            },
                            "subtitle": "President and Chief Executive Officer at MasterCard",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/thomas-kurian-469b6219?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Thomas Kurian",
                            },
                            "subtitle": "CEO at Google Cloud",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/dara-khosrowshahi-70949862?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Dara Khosrowshahi",
                            },
                            "subtitle": "CEO at Uber",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/heathergrahamtalent?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Heather Graham",
                            },
                            "subtitle": "Hakkasan",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/brianchesky?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Brian Chesky",
                            },
                            "subtitle": "Co-founder, CEO @ Airbnb",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/jennifer-lawrence-33b02827?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Jennifer Lawrence",
                            },
                            "subtitle": "Event Planner/Promoter at Queen of Hearts Entertainment",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/joy-colantone-b19aa1115?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Joy Colantone",
                            },
                            "subtitle": "Managing Director at JPMorgan Chase & Co.",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/donald-trump-jr-4454b862?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Donald Trump Jr.",
                            },
                            "subtitle": "Executive Vice President at The Trump Organization",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/professorporter?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Michael Porter",
                            },
                            "subtitle": "Professor at Harvard Business School",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/mikebloomberg?trk=public_profile_browsemap_profile-result-card_result-card_full-click",
                                "link_text": "Mike Bloomberg",
                            },
                            "subtitle": "Entrepreneur, philanthropist, and three-term mayor of New York City.",
                        },
                    ]
                },
                "samename": {
                    "people": [
                        {
                            "card": {
                                "link_page": "https://de.linkedin.com/in/barack-obama-0366aa1b0?trk=public_profile_samename_profile_profile-result-card_result-card_full-click",
                                "link_text": "Barack Obama",
                            },
                            "location": "Berlin Area, Germany",
                            "subtitle": "CEO bei Siemens",
                        },
                        {
                            "card": {
                                "link_page": "https://www.linkedin.com/in/barack-obama-8367661a8?trk=public_profile_samename_profile_profile-result-card_result-card_full-click",
                                "link_text": "Barack Obama",
                            },
                            "location": "Houston, Texas Area",
                            "subtitle": "Student at Harvard Law School",
                        },
                    ]
                },
            },
        }
        for k, v in expected.items():
            self.assertEqual(v, lkn.data[k])


if __name__ == '__main__':
    unittest.main()
