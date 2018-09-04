from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """
    用户信息表
    """
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.png', verbose_name='头像')
    reg_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class Blog(models.Model):
    """
    博客表
    """
    nid = models.AutoField(primary_key=True)
    user = models.OneToOneField('UserInfo')
    title = models.CharField(max_length=64, verbose_name='个人博客标题')
    site = models.CharField(max_length=32, unique=True, verbose_name='个人主页地址')
    theme = models.CharField(max_length=32, verbose_name='个人博客主题')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'


class Category(models.Model):
    """
    个人博客文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='分类标题')
    blog = models.ForeignKey(to='Blog', to_field='nid')  # 外键关联博客，一个博客可有多个分类

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'


class Tag(models.Model):
    """
    标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='标签名')
    blog = models.ForeignKey(to='Blog', to_field='nid')  # 所属博客

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='标题')
    abstract = models.CharField(max_length=256, verbose_name='摘要')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    category = models.ForeignKey(to='Category', to_field='nid', null=True)
    tags = models.ManyToManyField(
        blank=True,
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag'),  # 注意顺序！
    )
    user = models.ForeignKey(to='UserInfo', to_field='nid')

    def __str__(self):
        return self.title

    def get_tags(self):
        return ', '.join([tag.title for tag in self.tags.all()])

    get_tags.short_description = '标签'

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to='Article', to_field='nid')

    class Meta:
        verbose_name = '文章详情'
        verbose_name_plural = '文章详情'


class Article2Tag(models.Model):
    """
    文章和标签关系表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid')
    tag = models.ForeignKey(to='Tag', to_field='nid')

    class Meta:
        unique_together = (('article', 'tag'), )


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid')
    article = models.ForeignKey(to='Article', to_field='nid')
    is_up = models.BooleanField()

    class Meta:
        unique_together = (('article', 'user'), )


class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid')
    article = models.ForeignKey(to='Article', to_field='nid')
    content = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True)

    def __str__(self):
        return self.content








