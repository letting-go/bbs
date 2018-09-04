from django.contrib import admin
from blog.models import UserInfo, Blog, Category, Tag,\
    Article, ArticleDetail, Article2Tag, ArticleUpDown, Comment
# Register your models here.


@admin.register(UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nid', 'username', 'phone', 'avatar', 'reg_time')
    exclude = ('password', )
    empty_value_display = '-empty-'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'site', 'theme')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'blog')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'blog')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'abstract', 'create_time',
                    'category', 'get_tags', 'user')
    date_hierarchy = 'create_time'


@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ('nid', 'content', 'article')
    search_fields = ('content', )


@admin.register(Article2Tag)
class Article2TagAdmin(admin.ModelAdmin):
    list_display = ('nid', 'article', 'tag')


@admin.register(ArticleUpDown)
class ArticleUpDownAdmin(admin.ModelAdmin):
    list_display = ('nid', 'user', 'article', 'is_up')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('nid', 'user', 'article',
                    'content', 'create_time', 'parent_comment')