"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from blog import views
from haystack.views import search_view_factory


urlpatterns = [
    # haystack 搜索
    url(r'^search/$', views.MySearchView(), name='haystack_search'),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout),
    url(r"^login/$", views.login, name='login'),
    url(r'^pc-geetest/register/$', views.get_capchar),
    url(r'^signup/$', views.signup, name='signup'),
    # 查看文章
    url(r'^(?P<site>\w+)/articles/(?P<article_id>\d+)/$', views.get_article, name='get_article'),
    # 每个用户的home主页
    url(r'^(?P<site>\w+)/$', views.home, name='home'),
    # 写新文章
    url(r'^articles/new/$', views.new_article, name='new_article'),
    # 用户上传图片
    url(r'^pics/upload/$', views.upload_pic, name='upload_pic'),

    # 查看归档/时间线
    url(r'^(?P<site>\w+)/archives/$', views.archives_detail, name='archives'),
    # 查看分类
    url(r'^(?P<site>\w+)/categories/$', views.categories_, name='categories'),
    # 查看分类详情
    url(r'^(?P<site>\w+)/categories/(?P<category>\w+)/$', views.categories_detail, name='category_detail'),
    # 查看标签
    url(r'^(?P<site>\w+)/tags/$', views.tags_, name='tags'),
    # 查看标签详情
    url(r'^(?P<site>\w+)/tags/(?P<tag>\w+)/$', views.tags_detail, name='tag_detail'),
    # 个人资料
    url(r'^(?P<site>\w+)/about/$', views.about_detail, name='about'),


    url(r'^ppp$', views.aaa)

]
# 404
handler404 = views.page_not_found
handler500 = views.page_error
