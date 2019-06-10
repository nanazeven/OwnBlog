from django.db import models
from django.utils import timezone
from django.conf import settings
from blog.models import Article


# Create your models here.


class Comment(models.Model):
    text = models.TextField('内容', max_length=300)
    pub_time = models.DateTimeField('评论时间', default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="评论人", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name="父评论", blank=True,null=True, on_delete=models.CASCADE)
    is_delete = models.BooleanField('是否删除',default=False,)

    def __str__(self):
        return self.text