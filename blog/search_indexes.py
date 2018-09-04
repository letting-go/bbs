#! /usr/bin/env python
# -*- coding: utf-8 -*-
# author: "Dev-L"
# file: search_indexes.py.py
# Time: 2018/9/2 19:50

from haystack import indexes
from blog.models import ArticleDetail


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    article = indexes.CharField(model_attr='article')

    def get_model(self):
        return ArticleDetail

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

