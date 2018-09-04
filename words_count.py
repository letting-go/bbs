#! /usr/bin/env python
# -*- coding: utf-8 -*-
# author: "Dev-L"
# file: aaaa.py
# Time: 2018/8/28 21:48
import re

text = """
style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”
style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”style=”margin: 20px 0; line-height: 3”"""

cnt = 0
# 匹配中文
chi = re.findall(r'[\u4E00-\u9FFF]', text)
text = re.sub(r'[\u4E00-\u9FFF]', '', text)
# print(text)
lines = text.split('\n')
for line in lines:
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~，。：？‘”’“（）=—；！?':
        line = line.replace(ch, ' ')
    cnt += len(line.split())

print(cnt+len(chi))