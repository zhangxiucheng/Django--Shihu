from django import template
from ..forms import CommentForm
from ..models import Comment

register = template.Library()


@register.inclusion_tag('./inclusions/_form.html', takes_context=True)
def show_comment_form(context, answer, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'answer': answer,
    }


@register.inclusion_tag('./inclusions/_list.html', takes_context=True)
def show_comments(context, answer, request):
    comment_list = Comment.objects.filter(post=answer)
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
        'answer': answer,
        'request': request,
    }
