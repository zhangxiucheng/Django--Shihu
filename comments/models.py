from django.db import models
from blog.models import Answer
from login.models import User
# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    # 创建评论时间为当前系统时间,应改为utc/网络 时间
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
