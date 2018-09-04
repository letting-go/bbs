import json
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from geetest import GeetestLib
from blog import models, forms
from bbs import settings
from haystack.views import SearchView


# Create your views here.


@login_required
def index(request):
    return render(request, 'base.html')


# 极验 验证码
pc_geetest_id = settings.pc_id
pc_geetest_key = settings.pc_key


def get_capchar(request):
    """
    获取极验验证码
    """
    user_id = request.session.get('user_id', '')
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session['user_id'] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def login(request):
    # next_url = request.GET.get('next', None)
    # print(next_url)
    # next = '<input type="text" id="next" name="next" style="display: none" value=%s>' % next_url
    if request.method == 'POST':
        # 初始化一个给AJAX返回的数据   默认返回错误响应
        ret = {'status': -1, 'msg': None}
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.GET.get('next')

        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session['user_id']

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码通过
            # 使用auth模块认证
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                auth.login(request, user_obj)
                ret['status'] = '0'
                ret['msg'] = next if next else '/%s/' % request.user.blog.site
            else:
                # 用户名不存在或密码错误
                ret['msg'] = '用户名不存在或密码错误'
        else:
            ret['status'] = -2
            ret['msg'] = '验证码错误'
        return JsonResponse(ret)
    return render(request, 'login.html')


def signup(request):
    auth.logout(request)
    if request.method == 'POST':
        # print(request.POST)
        ret = {'status': -1, 'msg': ''}
        form_obj = forms.RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop('re_password')
            avatar_img = request.FILES.get('avatar')
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret['status'] = 0
            ret['msg'] = '/index/'
            return JsonResponse(ret)
        else:
            # 表单验证不通过
            print(form_obj.errors)
            ret['msg'] = form_obj.errors
            return JsonResponse(ret)
    # get请求
    form_obj = forms.RegForm()

    return render(request, 'signup.html', {'form_obj': form_obj})


def home(request, site):
    """
    展示用户主页
    :param site: 用户个人主页
    """

    blog = get_object_or_404(models.Blog, site=site)

    articles = models.Article.objects.filter(user=blog.user).order_by('-nid')
    if not articles:  # 如果该用户没有写过文章，直接返回
        article_list = []
        return render(request, 'home.html', locals())
    # 分页
    from blog.pagination import Pagination
    page_num = request.GET.get('page', 1)
    pager = Pagination(page_num, len(articles), site, per_page=10, max_show=11)
    # print(pager.current_page)
    # print(pager.start, pager.end)

    article_list = articles[pager.start:pager.end]
    page_nav_html = pager.page_nav_html()
    # print(article_list)
    # print(page_nav_html)
    return render(request, 'home.html', locals())


def get_article(request, site, article_id):
    """
    :param site: 用户主页
    :param article_id: 文章编号
    """
    blog = get_object_or_404(models.Blog, site=site)
    article = get_object_or_404(models.Article, nid=int(article_id), user=blog.user)
    tags = [tag.title for tag in article.tags.all()]
    article_next = models.Article.objects.filter(user=article.user, nid__gt=int(article_id)).first()
    article_pre = models.Article.objects.filter(user=article.user, nid__lt=int(article_id)).last()

    return render(request, 'article.html', locals())


@login_required
def new_article(request):
    site = request.user.blog.site
    categories = models.Category.objects.filter(blog__user=request.user)
    tags = models.Tag.objects.filter(blog__user=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tags_str = json.loads(request.POST.get('tags'))
        tags = list(map(lambda i: int(i), tags_str))

        # 处理用户新增的分类和标签, 优先使用新增的分类
        new_add_category = request.POST.get('new_add_category')
        new_add_tags = json.loads(request.POST.get('new_add_tags'))
        print(new_add_category, new_add_tags)


        from django.db import transaction  # 开启事务
        with transaction.atomic():
            try:
                if new_add_category:  # 新增分类
                    category_obj = models.Category.objects.create(title=new_add_category, blog=request.user.blog)
                else:
                    category_obj = models.Category.objects.get(nid=int(category))

                new_article_obj = models.Article.objects.create(title=title, abstract=content[:150],
                                                                category=category_obj, user=request.user)
                new_article_detail = models.ArticleDetail.objects.create(content=content, article=new_article_obj)

                # 由于多对多是基于第三张表的，新建的时候略麻烦，要手动创建多对多关联关系的记录
                if tags:
                    tag_obj_list = models.Tag.objects.extra(where=['nid in %s'], params=[tags])
                    for tag_obj1 in tag_obj_list:  # 原有标签
                        models.Article2Tag.objects.create(article=new_article_obj, tag=tag_obj1)

                new_add_tag_obj_list = []  # 新增标签对象列表
                for new_add_tag in new_add_tags:
                    new_add_tag_obj_list.append(models.Tag.objects.create(title=new_add_tag, blog=request.user.blog))
                for tag_obj2 in new_add_tag_obj_list:  # 新增标签
                    models.Article2Tag.objects.create(article=new_article_obj, tag=tag_obj2)

            except Exception as e:
                print(e)
                ret = {
                    'status': -1,
                    'msg': 'Error!'
                }
                return JsonResponse(ret)
        ret = {
            'status': 0,
            'msg': '/%s/' % site
        }
        return JsonResponse(ret)
    return render(request, 'new_article.html', locals())


@login_required
def upload_pic(request):
    site = request.user.blog.site
    ret = {
        "success": 0,  # 0表示上传失败;1表示上传成功
        "message": "提示的信息",
        "url": "图片地址"  # 上传成功时才返回
    }
    pic = request.FILES.get('editormd-image-file')
    # print(dir(pic))
    import os
    from bbs import settings
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, site)):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, site))
        print('1 dir create...')
    target_path = os.path.join(settings.MEDIA_ROOT, site, pic.name)
    with open(target_path, 'wb') as f:
        for chunk in pic.chunks():
            f.write(chunk)

    url_token = get_url_token(os.path.abspath(target_path), pic.name)
    ret['success'] = 1 if url_token else 0
    ret['url'] = url_token
    ret['msg'] = 'Success!' if url_token else 'Error!'

    return JsonResponse(ret)


def get_url_token(file_path, file_name):
    from qiniu import Auth, put_file, etag
    import qiniu.config
    # 需要填写你的 Access Key 和 Secret Key
    access_key = settings.access_key
    secret_key = settings.secret_key
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'pics'
    # 上传到七牛后保存的文件名
    key = file_name
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600*24*3600)
    # 要上传文件的本地路径
    localfile = file_path
    ret, info = put_file(token, key, localfile)
    url = 'http://pdwd5ogz2.bkt.clouddn.com/' + key
    # print(url)
    try:
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
    except:
        return None
    return url


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '404.html')


def archives_detail(request, site):
    """归档/时间线 详情"""
    blog = models.Blog.objects.get(site=site)

    articles = models.Article.objects.filter(user=blog.user).order_by('-create_time').values()

    if not articles:  # 如果该用户没有写过文章，直接返回
        article_list = []
        return render(request, 'archives_detail.html', locals())
    # 分页
    from blog.pagination import Pagination
    page_num = request.GET.get('page', 1)
    pager = Pagination(page_num, len(articles), request.path[1:], per_page=10, max_show=11)
    # print(pager.current_page)
    # print(pager.start, pager.end)

    article_list = articles[pager.start:pager.end]
    page_nav_html = pager.page_nav_html()
    # print(article_list)
    # print(page_nav_html)
    return render(request, 'archives_detail.html', locals())


def categories_(request, site):
    """"分类"""
    blog = models.Blog.objects.get(site=site)
    category_obj_list = models.Category.objects.filter(blog=blog)
    return render(request, 'category.html', locals())


def categories_detail(request, site, category):
    """"分类详细"""
    blog = get_object_or_404(models.Blog, site=site)
    category_obj = get_object_or_404(models.Category, blog=blog, title=category)
    return render(request, 'category_detail.html', locals())


def tags_(request, site):
    """标签"""
    blog = get_object_or_404(models.Blog, site=site)
    tag_obj_list = models.Tag.objects.filter(blog=blog)
    return render(request, 'tags.html', locals())


def tags_detail(request, site, tag):
    """标签详细"""
    blog = get_object_or_404(models.Blog, site=site)
    tag_obj = get_object_or_404(models.Tag, blog=blog, title=tag)
    return render(request, 'tag_detail.html', locals())


def about_detail(request, site):
    """个人资料"""
    return HttpResponse('ok')


# haystack检索
from django.conf import settings
from django.shortcuts import render
from haystack.query import EmptySearchQuerySet

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class MySearchView(SearchView):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()


def aaa(request):
    return HttpResponse('test')