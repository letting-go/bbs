#! /usr/bin/env python
# -*- coding: utf-8 -*-
# author: "Dev-L"
# file: remove_sapce_line.py
# Time: 2018/8/24 12:39

import os

filename = 'tag_detail.html'

with open(filename, 'r', encoding='utf8') as r:
    with open('%s.bak' % filename, 'w', encoding='utf8') as w:
        for line in r:
            if line.strip():
                w.write(line)
os.remove(filename)
os.rename('%s.bak' % filename,  filename)