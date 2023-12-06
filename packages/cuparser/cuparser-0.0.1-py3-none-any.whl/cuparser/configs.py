# -*- coding:utf-8 -*-
# author: kusen
# email: 1194542196@qq.com
# date: 2023/11/28


import re

UNIT_MAP = {
    't': 10,
    'h': 100,
    'K': 1000,
    'tK': 10000,
    'hK': 100000,
    'M': 1000000,
    'tM': 10000000,
    'hM': 100000000,
    'G': 1000000000,
    'tG': 10000000000,
    'T': 100000000000,
    'tP': 1000000000000,
    'hP': 10000000000000,
}

ALL_UNIT_REGEX = [
    (r'万亿', 'T'),
    (r'千亿', 'hG'),
    (r'百亿', 'tG'),
    (r'十亿', 'G'),
    (r'亿', 'hM'),
    (r'千万', 'tM'),
    (r'百万', 'M'),
    (r'十万', 'hK'),
    (r'万', 'tK'),
    (r'千', 'K'),
    (r'百', 'h'),
    (r'十', 't'),
]
ALL_UNIT_REGEX = [(re.compile(regex), unit) for regex, unit in ALL_UNIT_REGEX]

NUMBER_REGEX = re.compile(r'\d+[(,\d{3})]*[(\\.\d+)]*')
