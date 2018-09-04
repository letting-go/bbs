#! /usr/bin/env python
# -*- coding: utf-8 -*-
# author: "Dev-L"
# file: pagination.py
# Time: 2018/8/27 11:32


class Pagination:
    def __init__(self, current_page, total_cnt, site, per_page=10, max_show=10):
        """
        :param current_page: 当前页码
        :param total_cnt: 数据总数
        :param base_url: url前缀
        :param per_page: 每页显示条数
        :param max_show: 底部页码导航显示条数
        """
        try:
            current_page = int(current_page)
            if current_page == 0:
                current_page = 1
        except Exception:
            current_page = 1
        self.total_cnt = total_cnt
        self.url = site
        self.per_page = per_page
        self.max_show = max_show
        self.page_cnt = total_cnt // per_page + 1 if total_cnt % per_page else total_cnt // per_page  # 总页数
        self.current_page = current_page if current_page < self.page_cnt else self.page_cnt
        self.nav_half_show = (self.max_show-1)//2

    @property
    def start(self):
        return (self.current_page-1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

    def page_nav_html(self):
        show_start = max(1, self.current_page-self.nav_half_show)
        show_end = min(self.page_cnt, self.current_page+self.nav_half_show)
        if self.current_page <= self.nav_half_show:
            show_end = min(self.max_show, self.page_cnt)
        if self.current_page + self.nav_half_show >= self.page_cnt:
            show_start = max(self.page_cnt - self.max_show + 1, 1)
        # 生成分页器html
        li = []
        # 首页
        li.append('<li><a href="/%s?page=%s" aria-label="Previous">'
                  '<span aria-hidden="true">«</span></a></li>' % (self.url, 1))
        # 上一页
        if self.current_page == 1:
            li.append('<li class="disabled"><a href="#">上一页</a></li>')
        else:
            li.append('<li><a href="/%s?page=%s">上一页</a></li>' % (self.url, self.current_page - 1))

        # 页码列表
        for i in range(show_start, show_end + 1):
            if i == self.current_page:
                li.append('<li class="active"><a href="/%s?page=%s">%s</a></li>' % (self.url, i, i))
            else:
                li.append('<li><a href="/%s?page=%s">%s</a></li>' % (self.url, i, i))

        # 下一页
        if self.current_page == self.page_cnt:
            li.append('<li class="disabled"><a href="#">下一页</a></li>')
        else:
            li.append('<li><a href="/%s?page=%s">下一页</a></li>' % (self.url, self.current_page + 1))

        # 尾页
        li.append(
            '<li><a href="/%s?page=%s" aria-label="Next">'
            '<span aria-hidden="true">»</span></a></li>' % (self.url, self.page_cnt))
        return ''.join(li)
