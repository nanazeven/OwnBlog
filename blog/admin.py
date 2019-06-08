from django.contrib import admin
from blog.models import Article, Tag
from comments.models import Comment
from accounts.models import BlogUser
# Register your models here.
class ArtAdminModel(admin.ModelAdmin):
    list_display = ['title', 'pub_time','author']
admin.site.register(Article, ArtAdminModel)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(BlogUser)
