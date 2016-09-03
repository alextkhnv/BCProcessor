from django.contrib import admin
from blog.models import Article, Comment

# Register your models here.
class ArticleInline(admin.StackedInline):
    model = Comment
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'user']
    inlines = [ArticleInline]
    list_filter = ['date']


admin.site.register(Article, ArticleAdmin)
