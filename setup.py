#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from iparse import VERSION

setup(
    name='iparse',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.tpl', '*.md']},
    author='lihe',
    author_email='imanux@sina.com',
    url='https://github.com/coghost/iparse',
    description='parser of bs4 with yaml config support',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='GPL',
    install_requires=[
        'logzero', 'PyYAML', 'stringcase', 'beautifulsoup4'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/coghost/iparse/issues',
        'Source': 'https://github.com/coghost/iparse',
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['parse', 'beautifulsoup4', 'bs4', 'yaml'],
)
