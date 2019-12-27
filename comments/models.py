from django.db import models
from blog.models import Answer
from login.models import User
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField()
    # 创建评论时间为当前系统时间,应改为utc/网络 时间
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Answer, on_delete=models.CASCADE)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    def __str__(self):
        return self.body[:20]

    class MPTTMeta:
        order_insertion_by = ['created_time']
