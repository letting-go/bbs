#! /usr/bin/env python
# -*- coding: utf-8 -*-
# author: "Dev-L"
# file: mytags.py
# Time: 2018/8/7 10:29
import re
from django.template import Library

register = Library()


@register.filter(name='get_d')
def get_d(obj, item):
    return obj[item]


@register.filter(name='get_label')
def get_label(obj):
    return obj.label


@register.filter(name='get_id_for_label')
def get_id_for_label(obj):
    return obj.id_for_label


@register.filter(name='get_errors')
def get_errors(obj):
    return obj.errors[0] if obj.errors else ''


@register.filter(name='count_words')
def count_words(text):
    """
     统计文本字数
    """
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

    return cnt + len(chi)


@register.filter(name='get_read_time')
def get_read_time(words_count):
    """
     阅读时间
    """
    return words_count // 180 + (1 if words_count % 150 else 0)


@register.filter(name='get_style')
def get_style(size):
    """
    根据size计算字体大小，size越大，字体颜色越深，字号越大
    font - size: 30px; color:  # 111
   8 ---> 12px      20---> 30px
    """
    if size < 5:
        style = 'font-size: 12px; color: #ccc'
    elif size < 10:
        style = 'font-size: 18px; color: #999'
    elif size < 20:
        style = 'font-size: 24px; color: #666'
    elif size < 40:
        style = 'font-size: 30px; color: #222'
    else:
        style = 'font-size: 36px; color: #111'
    return style
