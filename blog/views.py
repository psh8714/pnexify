import random
import time
import uuid
from http.client import responses
from idlelib.debugger_r import idb_adap_oid
from itertools import count
from tabnanny import check

from django.db.models import Q
from django.db.models.aggregates import Count
from django.db.models.expressions import result
from django.db.models.fields import return_None
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.text import slugify

from mycodes.settings import MEDIA_URL
from .forms import *
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import *
from django.shortcuts import get_object_or_404
import datetime
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import random
import requests
from django.core.mail import send_mail
from django.contrib import messages
from django.db import transaction


# Create your views here.
def index(request):
    if Post.objects.exists():
        post = random.choice(list(Post.published.all()))
    else:
        post = 'empty page'
    text1, created1 = Text.objects.get_or_create(text_name='index_blue_title')
    text2, created2 = Text.objects.get_or_create(text_name='index_big_title')
    text3, created3 = Text.objects.get_or_create(text_name='index_small_description')
    text4, created4 = Text.objects.get_or_create(text_name='index_see_posts')
    text5, created5 = Text.objects.get_or_create(text_name='index_about_us')
    text6, created6 = Text.objects.get_or_create(text_name='index_new_post')
    text7, created7 = Text.objects.get_or_create(text_name='index_new_posts')
    text8, created8 = Text.objects.get_or_create(text_name='index_see_more')
    text9, created9 = Text.objects.get_or_create(text_name='index_write_title')
    text10, created10 = Text.objects.get_or_create(text_name='index_write_description')
    text11, created11 = Text.objects.get_or_create(text_name='index_write_button')
    text12, created12 = Text.objects.get_or_create(text_name='index_newpost_tag')
    notif, created13 = Text.objects.get_or_create(text_name='index_NOTIFICATION')
    context = {
        'post': post,
        'text1': text1,
        'text2': text2,
        'text3': text3,
        'text4': text4,
        'text5': text5,
        'text6': text6,
        'text7': text7,
        'text8': text8,
        'text9': text9,
        'text10': text10,
        'text11': text11,
        'text12': text12,
        'notif': notif,
    }
    return render(request, "blog/index.html", context)


def about_us_view(request):
    return render(request, "partials/about_us.html")


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category).order_by('-total_likes', '-created')
    else:
        posts = Post.published.all().order_by('-total_likes', '-created')
    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.headers.get('HX-Request'):
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.headers.get('HX-Request'):
        return render(request, 'blog/htmx_list.html', {'posts': posts, 'category': category, })
    text1, created = Text.objects.get_or_create(text_name='post_list_title')
    context = {
        'posts': posts,
        'category': category,
        'text1': text1,
    }
    return render(request, "blog/list.html", context)


# class PostList(ListView):
#     paginate_by = 3
#     context_object_name = 'posts'
#     template_name = 'blog/list.html'
#     queryset = Post.published.all()


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    similar_posts = Post.published.exclude(pk=post.pk).annotate(
        common_tags=Count("tags", filter=Q(tags__in=post.tags.all()))).filter(common_tags__gt=0).order_by(
        '-common_tags', 'publish')[:3]

    context = {
        'post': post,
        'new_date': datetime.datetime.now(),
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
    }
    return render(request, "blog/detail.html", context)


# class PostDetail(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#     extra_context = {
#         'new_date': datetime.datetime.now()
#     }


def ticket_view(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"you have a message of:\n{cd['name']}\nmessage:\n{cd['message']}\nphone_number:{cd['phone']}"
            send_mail(cd['subject'], message, "parham.nadim7777@gmail.com", ["parham.nadim777@gmail.com"])
            messages.success(request, 'با موفقیت ارسال شد')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


# @require_POST
# @login_required
# def comment_view(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
#     comment = None
#     form = CommentForm(data=request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.user = request.user
#         comment.save()
#         messages.info(request, 'کامنت شما پس از تایید ادمین منتشر میشود')
#         return redirect(post.get_absolute_url())
#     context = {
#         'post': post,
#         'comment': comment,
#         'form': form
#     }
#     return render(request, 'blog/list.html', context)


@login_required
@require_POST
def comment(request):
    post_slug = request.POST.get('post_slug')
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST)
    next_url = request.POST.get('next')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.post = post
        obj.user = request.user
        obj.save()
        comment_html = render_to_string(
            "forms/comment_item.html",
            {'comment': obj},
            request=request
        )
        return JsonResponse({"comment_html": comment_html, "next_url": next_url})


def search_view(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'description')).filter(search=query)
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'blog/search.html', context)


@login_required
def profile_view(request):
    user = User.objects.prefetch_related('followers__followings').get(id=request.user.id)
    d_profile = MEDIA_URL + 'profile_image/avatar.png'
    posts_qs = Post.objects.filter(author=request.user)
    comments_qs = CommentModel.objects.filter(post__author=request.user)

    post_paginator = Paginator(posts_qs, 3)
    comment_paginator = Paginator(comments_qs, 7)

    post_page_number = request.GET.get('post_page', 1)
    comment_page_number = request.GET.get('comment_page', 1)

    try:
        posts = post_paginator.page(post_page_number)
    except PageNotAnInteger:
        posts = post_paginator.page(1)
    except EmptyPage:
        posts = post_paginator.page(post_paginator.num_pages)

    try:
        comments = comment_paginator.page(comment_page_number)
    except PageNotAnInteger:
        comments = comment_paginator.page(1)
    except EmptyPage:
        comments = comment_paginator.page(comment_paginator.num_pages)

    text1, created1 = Text.objects.get_or_create(text_name='profile_parple_title')
    text2, created2 = Text.objects.get_or_create(text_name='profile_title')
    text3, created3 = Text.objects.get_or_create(text_name='profile_followers')
    text4, created4 = Text.objects.get_or_create(text_name='profile_following')
    text5, created5 = Text.objects.get_or_create(text_name='profile_posts_title')
    text6, created6 = Text.objects.get_or_create(text_name='profile_comments_title')
    text7, created7 = Text.objects.get_or_create(text_name='profile_description')

    context = {
        'posts': posts,
        'comments': comments,
        'profile': d_profile,
        'user': user,
        'text1': text1,
        'text2': text2,
        'text3': text3,
        'text4': text4,
        'text5': text5,
        'text6': text6,
        'text7': text7,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def new_post_view(request):
    if request.method == "POST":
        form = NewPost(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = (
                f"{uuid.uuid4().hex[:6]}"
            )

            image_formset = ImageFormSet(
                request.POST,
                request.FILES,
                instance=post,
            )
            if image_formset.is_valid():
                with transaction.atomic():
                    post.save()
                    image_formset.instance = post
                    image_formset.save()
                    form.save_m2m()
                # images = request.FILES.getlist('images')
                # for image in images:
                #     ImagePost.objects.create(image_file=image, post=post)
                #     -------------
                # img1 = form.cleaned_data.get('image1')
                # img2 = form.cleaned_data.get('image2')
                # if img1:
                #     ImagePost.objects.create(image_file=img1, post=post)
                # if img2:
                #     ImagePost.objects.create(image_file=img2, post=post)

                # if post.category == 'WIC':
                #     detail_form = ProjectDetailForm(request.POST)
                #     if detail_form.is_valid():
                #         detail_obj = detail_form.save(commit=False)
                #         detail_obj.post = post
                #         detail_obj.save()
                #         detail_obj.technologies.set(
                #             detail_form.cleaned_data['technologies']
                #         )
                ProjectDetail.objects.create(post=post)

                return redirect('blog:profile_view')
    else:
        form = NewPost()
        image_formset = ImageFormSet(
        )
    text1, created1 = Text.objects.get_or_create(text_name='add_post_title')
    text2, created2 = Text.objects.get_or_create(text_name='add_post_description')
    context = {
        'form': form,
        'image_formset': image_formset,
        'text1': text1,
        'text2': text2,
    }
    return render(request, 'forms/new_post.html', context)


def edit_post(request, post_slug):
    post_obj = get_object_or_404(Post, slug=post_slug, author=request.user)
    detail_obj = get_object_or_404(ProjectDetail, post = post_obj)
    if request.method == "POST":
        form = NewPost(request.POST, request.FILES, instance=post_obj)
        detail_form = ProjectDetailForm(request.POST, instance=detail_obj)

        image_formset = ImageFormSet(
            request.POST,
            request.FILES,
            instance=post_obj
        )
        if form.is_valid() and image_formset.is_valid() and detail_form.is_valid():
            post_obj = form.save(commit=False)
            post_obj.author = request.user
            detail_obj = detail_form.save(commit=False)
            detail_obj.post = post_obj
            # image1 = form.cleaned_data['image1']
            # image2 = form.cleaned_data['image2']
            # if image1:
            #     ImagePost.objects.create(image_file=image1, post=post_obj, title=post_obj.title)
            # if image2:
            #     ImagePost.objects.create(image_file=image2, post=post_obj, title=post_obj.title)

            with transaction.atomic():
                post_obj.save()
                image_formset.save()
                detail_obj.save()
                form.save_m2m()
            return redirect('blog:profile_view')
    else:
        form = NewPost(instance=post_obj)
        detail_form = ProjectDetailForm(instance=detail_obj)
        image_formset = ImageFormSet(instance=post_obj)
    text1, created1 = Text.objects.get_or_create(text_name='edit_post_title')
    text2, created2 = Text.objects.get_or_create(text_name='edit_post_description')
    context = {
        'form': form,
        'detail_form': detail_form,
        'post': post_obj,
        'image_formset': image_formset,
        'text1': text1,
        'text2': text2,
    }
    return render(request, 'forms/new_post.html',
                  context=context)


def delete_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == "POST":
        post.delete()
        return redirect('blog:profile_view')

    return render(request, 'forms/delete_post.html')


@login_required
def twit_view(request):
    twits = TwitModel.objects.all()
    my_twits = []
    another_twits = []
    for i in twits:
        if i.writer == request.user:
            my_twits.append(i)
        if i.writer != request.user:
            another_twits.append(i)

    if request.method == 'POST':
        form = TwitForm(request.POST)
        if form.is_valid():
            twit_obj = form.save(commit=False)
            twit_obj.writer = request.user
            twit_obj.save()
            return redirect('blog:twit_view')
    else:
        form = TwitForm()

    context = {
        'form': form,
        'twits': twits,
        'my_twits': my_twits,
        'another_twits': another_twits,
    }

    return render(request, 'forms/twit.html', context)


def delete_twit(request, twit_id):
    twit = get_object_or_404(TwitModel, id=twit_id)
    if request.method == "POST":
        twit.delete()
        return redirect('blog:twit_view')
    return render(request, 'forms/delete_twit.html')


# def log_in(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['name'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('welcome dear user')
#                 else:
#                     return HttpResponse('your account is not available')
#             else:
#                 return HttpResponse('username or password is not right')
#     else:
#         form = LoginForm()
#     return render(request, 'forms/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_user_done.html', {'user': user})
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/register_user.html', context)


def user_edit(request):
    user = request.user
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        formset = SkillFormSet(
            request.POST,
            queryset=Skill.objects.filter(user=user)
        )
        if user_form.is_valid() and formset.is_valid():
            user_form.save()
            skills = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for skill in skills:
                skill.user = user
                skill.save()
            return redirect('blog:profile_view')
    else:
        formset = SkillFormSet(
            queryset=Skill.objects.filter(user=user)
        )
        user_form = UserForm(instance=user)
    context = {
        'user_form': user_form,
        'formset': formset,
    }
    return render(request, 'registration/edit_user.html', context)


def user_info(request, user):
    user_ = get_object_or_404(User, id=user)
    user_skills = get_object_or_404(Skill, user=user_)
    user_posts = Post.published.filter(author_id=user)
    # user_posts = Post.published.filter(author_id=user)
    user_comments = user.comments.all()
    # user_comments = CommentModel.objects.filter(user_id=user)
    context = {
        'user': user_,
        'user_skills': user_skills,
        'user_posts': user_posts,
        'user_comments': user_comments
    }
    return render(request, 'partials/user_informations.html', context)


def to_do_list(request, pk=None, bol=None):
    if request.method == 'POST' and pk is None:
        form = ToDoListForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('blog:to_do_list')
    else:
        form = ToDoListForm()
    if pk is not None and bol == 'True':
        new_obj = get_object_or_404(ToDoList2, pk=pk)
        new_obj.situation = False
        new_obj.save()
        return redirect('blog:to_do_list')
    if pk is not None and bol == 'False':
        new_obj = get_object_or_404(ToDoList2, pk=pk)
        new_obj.situation = True
        new_obj.save()
        return redirect('blog:to_do_list')
    if ToDoList2.objects and pk is None:
        tasks = ToDoList2.objects.filter(user=request.user, situation=False).order_by('creat_time')
        f_tasks = ToDoList2.objects.filter(user=request.user, situation=True).order_by('creat_time')
        context = {
            'tasks': tasks,
            'form': form,
            'f_tasks': f_tasks
        }
        return render(request, 'forms/to_do_list.html', context)
    else:
        context = {
            'form': form,
        }
        return render(request, 'forms/to_do_list.html', context)


def delete_to_do_list(request, task_id):
    task = get_object_or_404(ToDoList2, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('blog:to_do_list')
    return render(request, 'forms/delete_to-do-list.html')


def login_or_register(request):
    return render(request, 'registration/login_or_register.html')


def login_(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(email=login_input).exists():
                username = User.objects.get(email=login_input).username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog:profile_view')
            elif User.objects.filter(phone_number=login_input).exists():
                username = User.objects.get(phone_number=login_input).username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog:profile_view')
            elif User.objects.filter(username=login_input).exists():
                username = User.objects.get(username=login_input).username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog:profile_view')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('p_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        post_likes_count = post.likes.count()
        response = {
            'liked': liked,
            'post_likes_count': post_likes_count,
        }
    else:
        response = {
            'error': 'Invalid post_id'
        }
    return JsonResponse(response)


@login_required
@require_POST
def follow_user(request):
    user_id = request.POST.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                user.followers.remove(request.user)
                followed = False
            else:
                user.followers.add(request.user)
                followed = True
            response = {
                'followed': followed,
                'follower_count': user.followers.count(),
                'following_count': user.followings.count(),
            }
            return JsonResponse(response)
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'User does not exist.'
            })
    return JsonResponse({
        'error': 'Invalid request.'
    })


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    user = request.user
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        if user in post.saver_accounts.all():
            user.saved_posts.remove(post)
            saved = False
        else:
            user.saved_posts.add(post)
            saved = True
        response = {
            'saved': saved,
        }
    else:
        response = {'errors': 'Invalid post_id'}
    return JsonResponse(response)


@login_required
def user_list(request, user_id=None, is_follow=None):
    if user_id is not None:
        t_user = get_object_or_404(User, id=user_id)
        if is_follow == 'follower':
            users = t_user.followers.annotate(post_count=Count('post'),
                                              comment_count=Count('comments')).order_by('-post_count',
                                                                                        '-comment_count')
            return render(request, 'user/user_list.html', {'users': users})
        if is_follow == 'following':
            users = t_user.followings.annotate(post_count=Count('post'),
                                               comment_count=Count('comments')).order_by(
                '-post_count',
                '-comment_count')
            return render(request, 'user/user_list.html', {'users': users})
        return None

    else:
        users = User.objects.filter(is_active=True).annotate(post_count=Count('post'),
                                                             comment_count=Count('comments')).order_by('-post_count',
                                                                                                       '-comment_count')
        return render(request, 'user/user_list.html', {'users': users})


def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'user/user_detail.html', {'user': user})


def l_ticket_view(request, user_id=None):
    if request.user.is_staff:
        tickets = LocalTicket.objects.filter(user_id=user_id)
        for ticket in tickets.all():
            ticket.read = True
            ticket.save()
    else:
        tickets = LocalTicket.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        form = LTicket(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            if request.user.is_staff:
                ticket.admin_wrote = True
                ticket.read = True
                ticket.user = get_object_or_404(User, id=user_id)
            else:
                ticket.admin_wrote = False
                ticket.user = request.user
            ticket.save()
            if request.user.is_staff:
                return redirect('blog:local_tickets_admin')
            else:
                return redirect('blog:local_ticket')
    else:
        form = LTicket()
    context = {
        'tickets': tickets,
        'form': form,
    }
    return render(request, 'forms/local_ticket.html', context=context)


def l_ticket_admin_view(request):
    if LocalTicket.objects.exists():
        users_ticket = LocalTicket.objects.select_related('user').distinct('user')
    else:
        users_ticket = None
    return render(request, 'partials/ticketlist_for_admin.html', {'users_ticket': users_ticket, })


def download_image(request, pk):
    image = get_object_or_404(ImagePost, pk=pk)
    return FileResponse(image.image_file.open(), as_attachment=True)

def header_color(request):
    return render(request, 'forms/header_changer.html')

import json
@login_required
def header_color_success(request):
    data = json.loads(request.body)
    colors = data['colors']
    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    color4 = colors[3]
    color5 = colors[4]
    color6 = colors[5]
    Theme.objects.update_or_create(
        user=request.user,
        defaults={
            'color1' : color1,
            'color2' : color2,
            'color3' : color3,
            'color4' : color4,
            'color5' : color5,
            'color6' : color6,
        }
    )

    return JsonResponse({
        "success": True
    })

def team_maker(request):
    pass