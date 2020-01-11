from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from django.utils import timezone
from mdeditor.fields import MDTextField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = MDTextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    # 作者  使用django内置应用
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    #点赞
    likecount = models.PositiveIntegerField(default=0)
    #user_like = models.ManyToManyField(User,  related_name="articles_like", blank=True)

    def  on_view(self):
        self.views += 1

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']

    """ 1.reverse的'blog:detail'对应blog应用下的name='detail'的方法(对应urls.py的name)
        2.reverse()方法会去解析'blog:detail'的url,解析规则是根据urls.py里的正则.
        3.根据正则规则,解析结果为post/255/,这样Post自己就生成了自己的url
        4.kwargs表示按照关键字传值将多余的传值用字典形式呈现
    """

    # 自定义获取路径方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 阅读量增加(粗略统计,同时访问被忽略)
    def increase_views(self):
        # 该函数每被调用一次 views+1
        self.views += 1
        # 只更新数据库中views字段的值
        self.save(update_fields=['views'])

    # 摘要逻辑 重写save()方法,保存到数据库之前进行一次过滤
    def save(self, *args, **kwargs):
        self.created_time = timezone.now()
        self.modified_time = self.created_time
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    excerpt = models.CharField(max_length=200, blank=True)
    body = MDTextField()
    tags = models.ManyToManyField(Tag, blank=True)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    views = models.PositiveIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def increase_views(self):
        # 该函数每被调用一次 views+1
        self.views += 1
        # 只更新数据库中views字段的值
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        self.created_time = timezone.now()
        self.modified_time = self.created_time
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Answer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:answer_detail', kwargs={'id': self.id})


#该部分负责人员认为必定存在更加节省数据库空间的实现方法，碍于时间有限，从头开始实现不现实
# 因为涉及到大范围的数据库结构修改，因此保留原始想法
#zxc
class Liked(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post,  on_delete=models.CASCADE)

        