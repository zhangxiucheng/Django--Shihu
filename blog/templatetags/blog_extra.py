from django import template
from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('./inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


@register.inclusion_tag('./inclusions/_archivers.html', takes_context=True)
def show_ars(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('./inclusions/_author.html')
def show_authors(author):
    return {
        'author_post_list': Post.objects.filter(author=author),
        'author_name': author.username,
    }


@register.inclusion_tag('./inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('./inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tags_list': Tag.objects.all(),
    }

