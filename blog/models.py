# coding: utf-8
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


# Create your models here.
class Article(models.Model):
    """文章"""
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    # body = MDTextField('正文')
    body = models.TextField('正文')
    pub_time = models.DateTimeField('发布时间', default=now)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('浏览量', default=0)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    author = models.CharField('作者', max_length=200)
    article_order = models.IntegerField('排序,数字越大越靠前', blank=False, null=False, default=0)
    # category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    # category = models.CharField('分类', max_length=200)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.id})

    def viewd(self):
        self.views += 1
        self.save(update_fields=['views'])

# class Category(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
