import datetime

from django import template

from ..models import Post, CommentModel, Text, Theme
from ..views import header_color

register = template.Library()


@register.simple_tag()
def post_number():
    return Post.published.count()


@register.simple_tag()
def comment_number():
    return CommentModel.objects.filter(active=True).count()


@register.simple_tag()
def last_post_publish():
    if Post.published.first():
        return Post.published.first().publish
    else:
        return ""


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=5):
    posts = Post.published.order_by('-publish')[:count]
    context = {
        'posts': posts
    }
    return context


@register.filter(name='add_class')
def add_class(field, classes):
    if hasattr(field, 'field'):
        field.field.widget.attrs['class'] = classes
    return field


@register.simple_tag()
def texts():
    title = Text.objects.get(text_name='SITE_TITLE')
    s_icon = Text.objects.get(text_name='header_search_icon')
    text1 = Text.objects.get(text_name='header_home')
    text2 = Text.objects.get(text_name='header_profile')
    text3 = Text.objects.get(text_name='header_posts')
    text4 = Text.objects.get(text_name='header_twits')
    text5 = Text.objects.get(text_name='header_add_post')
    text6 = Text.objects.get(text_name='header_about_us')
    text7 = Text.objects.get(text_name='header_contact_us')

    return {
        's_icon': s_icon,
        'title': title,
        'text1': text1,
        'text2': text2,
        'text3': text3,
        'text4': text4,
        'text5': text5,
        'text6': text6,
        'text7': text7,
    }


@register.simple_tag()
def head_color(user=None):
    DEFAULT_THEME = {
        "color1": "#7c3aed",
        "color2": "#a78bfa",
        "color3": "#0b1120",
        "color4": "#a78bfa",
        "color5": "#93c5fd",
        "color6": "#0f172a"
    }

    try:
        header_colors = Theme.objects.get(user=user)
        return header_colors
    except:
        header_colors = DEFAULT_THEME
        return header_colors
