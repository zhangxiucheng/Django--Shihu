from blog.models import Answer
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.utils import timezone
from .forms import CommentForm
from login.models import User
from .models import Comment
from notifications.signals import notify


def comment(request, id, reply=None):
    post = get_object_or_404(Answer, id=id)
    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    # 先把POST的内容过一遍markdown的渲染器
    # 这事是不是应该拿js在用户机器上做？
    # md = markdown.Markdown(extensions=[
    #    'markdown.extensions.extra',
    #    'markdown.extensions.codehilite',
    # ])
    # https://docs.djangoproject.com/zh-hans/3.0/ref/request-response/#django.http.QueryDict.__setitem__
    # rPOST = request.POST.copy()
    # rPOST.__setitem__("text", md.convert(rPOST.get("text")))
    if not request.session.get('is_login', None):
        return HttpResponse('请登录后操作')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_time = timezone.now()
            comment.post = post
            user = User.objects.get(name=request.session.get('user_name'))
            comment.user = user
            if reply:
                parent_comment = Comment.objects.get(id=reply)
                comment.parent_id = parent_comment.get_root().id
                comment.reply_to = parent_comment.user
                parent_user = User.objects.get(id=parent_comment.user.id)
                comment.save()
                if not parent_user == comment.user:
                    notify.send(
                        sender=user,
                        recipient=parent_user,
                        verb='replied',
                        target=post,
                        action_object=comment,
                    )
                return HttpResponse('200 OK')

            comment.save()
            author = User.objects.get(id=post.author.id)
            if not request.session.get('user_id', None) == post.author.id:
                notify.send(
                    sender=user,
                    recipient=author,
                    verb='commented',
                    target=post,
                    action_object=comment,
                )
            return redirect(post)
    elif request.method == "GET":
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': id,
            'parent_comment_id': reply,
        }
        return render(request, 'comments/reply.html', context)
