# from django.contrib import admin
# from django.core.mail import send_mail
#
# from .models import *
# from django.contrib.auth.admin import UserAdmin
#
#
# # Register your models here.
#
# def email_sender_publisher(modeadnim, request, queryset):
#     queryset.update(status=Post.Status.PUBLISHED)
#     for post in queryset:
#         message = f"hi \n {post.title} checked and published by admin"
#         send_mail("your post Published", message, "parham.nadim7777@gmail.com", [post.author.email])
#     modeadnim.message_user(request, 'successful action')
#
#
# email_sender_publisher.short_description = 'انتشار پست'
#
#
# def email_sender_rejecter(modeadnim, request, queryset):
#     queryset.update(status=Post.Status.REJECTED)
#     for post in queryset:
#         message = f"hi \n {post.title} checked and rejected by admin"
#         send_mail("your post Rejected", message, "parham.nadim7777@gmail.com", [post.author.email])
#     modeadnim.message_user(request, 'successful action')
#
#
# email_sender_rejecter.short_description = 'رد انتشار پست'
#
#
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'author_id', 'slug', 'status', 'publish',)
#     ordering = ('-publish',)
#     search_fields = ('title', 'slug')
#     list_filter = ('status', 'author')
#     fieldsets = (
#         ("اطلاعات اجباری", {
#             "fields": ("title", "author", "description"),
#         }),
#         ("تنظیمات پیشرفته", {
#             "classes": ("collapse",),
#             "fields": ("slug", "publish", "status", "category", 'total_likes', 'total_saves'),
#         }),
#     )
#     raw_id_fields = ('author',)
#     date_hierarchy = 'publish'
#     list_per_page = 10
#     list_editable = ('status',)
#     list_display_links = ('title',)
#     actions = [email_sender_publisher, email_sender_rejecter]
#
#
# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
#
# @admin.register(CommentModel)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'user', 'active', 'helpful', 'post', 'created']
#     list_filter = ['name', 'active']
#     list_editable = ['active','helpful']
#     search_fields = ['name', 'body', 'post__title']
#
#
# @admin.register(TwitModel)
# class TwitModelAdmin(admin.ModelAdmin):
#     list_display = ['title', 'writer', 'create_time', 'description']
#
#
# @admin.register(User)
# class UserAdmin(UserAdmin):
#     list_display = ['username', 'phone_number', 'notif']
#     fieldsets = UserAdmin.fieldsets + ((
#                                            'Additional Info', {
#                                            'fields': ('date_of_birth', 'city', 'phone_number', 'bio', 'tel_id', 'github_id', 'main_skill',
#                                                       'photo', 'followings', 'notif', 'verify', 'ostan')}
#                                        ),)
#
#
# @admin.register(ToDoList2)
# class ToDoListAdmin(admin.ModelAdmin):
#     list_display = ['user', 'description', 'deadline1']
#
#
# @admin.register(ImagePost)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ['post', 'title', 'image_file']
#
#
# @admin.register(LocalTicket)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ['ticket', 'user', 'admin_wrote']
#
#
# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ['user', 'skill', 'level', 'confirmed']
#
#
# @admin.register(Text)
# class TextAdmin(admin.ModelAdmin):
#     list_display = ['text_name', 's_description']
#
# @admin.register(Theme)
# class ThemeAdmin(admin.ModelAdmin):
#     list_display = ['user']
#
# @admin.register(ProjectDetail)
# class ProjectDetailAdmin(admin.ModelAdmin):
#     list_display = ['post']


# AI ------------------------------------------


from django.contrib import admin
from django.core.mail import send_mail
from django.db.models import Count, Sum
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    User,
    Post,
    Tag,
    CommentModel,
    ImagePost,
    Skill,
    ProjectDetail,
    Technology,
    TwitModel,
    ToDoList2,
    LocalTicket,
    Text,
    Theme,
    Team,
    TeamMember,
    TeamRequest
)


# ==========================
# Post Actions
# ==========================
@admin.action(description="انتشار پست‌های انتخاب شده")
def publish_posts(modeladmin, request, queryset):
    for post in queryset:
        post.status = Post.Status.PUBLISHED
        post.save(update_fields=['status'])
        if post.author.email:
            send_mail(
                "Your post published",
                f"Hi {post.title}, your post has been checked and published.",
                "your@email.com",
                [post.author.email],
            )
    modeladmin.message_user(
        request,
        "پست‌ها با موفقیت منتشر شدند."
    )


@admin.action(description="رد پست‌های انتخاب شده")
def reject_posts(modeladmin, request, queryset):
    for post in queryset:
        post.status = Post.Status.REJECTED
        post.save(update_fields=['status'])
        if post.author.email:
            send_mail(
                "Your post rejected",
                f"Hi {post.title}, your post has been rejected.",
                "your@email.com",
                [post.author.email],
            )
    modeladmin.message_user(
        request,
        "پست‌ها رد شدند."
    )


# ==========================
# Inline ها
# ==========================
class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    fields = (
        "skill",
        "level",
        "confirmed",
    )


class UserPostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = (
        "title",
        "status",
        "total_views",
        "total_likes",
        "publish",
    )
    readonly_fields = (
        "total_views",
        "total_likes",
    )
    show_change_link = True


class ImageInline(admin.TabularInline):
    model = ImagePost
    extra = 0
    fields = (
        "title",
        "image_file",
    )


class CommentInline(admin.TabularInline):
    model = CommentModel
    extra = 0
    fields = (
        "user",
        "name",
        "active",
        "helpful",
        "created",
    )
    readonly_fields = (
        "created",
    )


# ==========================
# User Admin
# ==========================

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "level",
        "verify",
        "post_count",
        "followers_count",
        "created",
    )
    list_filter = (
        "level",
        "verify",
        "ostan",
        "created",
    )
    search_fields = (
        "username",
        "email",
        "phone_number",
        "city",
    )
    readonly_fields = (
        "created",
        "last_login",
    )
    inlines = [
        SkillInline,
        UserPostInline,
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            "اطلاعات پروفایل",
            {
                "fields": (
                    "photo",
                    "phone_number",
                    "bio",
                    "date_of_birth",
                    "city",
                    "ostan",
                    "tel_id",
                    "github_id",
                    "main_skill",
                    "level",
                    "verify",
                    "notif",
                )
            }
        ),
    )

    def post_count(self, obj):
        return obj.post.count()

    post_count.short_description = "پست‌ها"

    def followers_count(self, obj):
        return obj.followers.count()

    followers_count.short_description = "دنبال‌کننده‌ها"

# ==========================
# Post Admin
# ==========================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "total_views",
        "total_likes",
        "total_saves",
        "publish",
    )
    list_filter = (
        "status",
        "category",
        "publish",
        "author__level",
    )
    search_fields = (
        "title",
        "description",
        "slug",
        "author__username",
    )
    readonly_fields = (
        "created",
        "updated",
        "total_views",
        "total_likes",
        "total_saves",
    )
    autocomplete_fields = (
        "author",
    )
    date_hierarchy = "publish"
    list_per_page = 20
    ordering = (
        "-publish",
    )
    actions = [
        publish_posts,
        reject_posts,
    ]
    inlines = [
        ImageInline,
        CommentInline,
    ]
    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "title",
                    "author",
                    "description",
                    "category",
                )
            }
        ),
        (
            "انتشار",
            {
                "fields": (
                    "status",
                    "publish",
                    "slug",
                )
            }
        ),
        (
            "آمار",
            {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "total_views",
                    "total_likes",
                    "total_saves",
                )
            }
        ),
        (
            "زمان‌ها",
            {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "created",
                    "updated",
                )
            }
        ),
    )

# ==========================
# Tag Admin
# ==========================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "post_count",
    )
    search_fields = (
        "name",
    )

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = "تعداد پست"

# ==========================
# Comment Admin
# ==========================
@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "post",
        "active",
        "helpful",
        "created",
    )
    list_filter = (
        "active",
        "helpful",
        "created",
    )
    search_fields = (
        "name",
        "body",
        "user__username",
        "post__title",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    autocomplete_fields = (
        "user",
        "post",
    )
    list_editable = (
        "active",
        "helpful",
    )

# ==========================
# Image Post Admin
# ==========================
@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "title",
        "image_preview",
    )
    search_fields = (
        "post__title",
    )
    autocomplete_fields = (
        "post",
    )

    def image_preview(self, obj):
        if obj.image_file:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:10px;">',
                obj.image_file.url
            )
        return "-"

    image_preview.short_description = "تصویر"

# ==========================
# Project Detail
# ==========================
class TechnologyInline(admin.TabularInline):
    model = ProjectDetail.technologies.through
    extra = 1

@admin.register(ProjectDetail)
class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "status",
        "project_url",
        "github_url",
    )
    search_fields = (
        "post__title",
    )
    autocomplete_fields = (
        "post",
    )

inlines = [
    TechnologyInline,
]


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    search_fields = (
        "name",
    )

# ==========================
# Team Admin
# ==========================
class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0
    fields = (
        "user",
        "role",
    )
    autocomplete_fields = (
        "user",
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "member_count",
        "created_at",
    )
    search_fields = (
        "name",
        "owner__username",
    )
    list_filter = (
        "created_at",
    )
    autocomplete_fields = (
        "owner",
    )
    readonly_fields = (
        "created_at",
    )
    inlines = [
        TeamMemberInline,
    ]

    def member_count(self, obj):
        return TeamMember.objects.filter(
            team=obj
        ).count()

    member_count.short_description = "تعداد اعضا"

# ==========================
# Team Request Admin
# ==========================
@admin.register(TeamRequest)
class TeamRequestAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "sender",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "team__name",
        "sender__username",
    )
    autocomplete_fields = (
        "team",
        "sender",
    )
    readonly_fields = (
        "created_at",
    )
    list_editable = (
        "status",
    )

# ==========================
# Local Ticket Admin
# ==========================
@admin.register(LocalTicket)
class LocalTicketAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "short_ticket",
        "read",
        "admin_wrote",
        "created",
    )
    list_filter = (
        "read",
        "admin_wrote",
        "created",
    )
    search_fields = (
        "user__username",
        "ticket",
    )
    autocomplete_fields = (
        "user",
    )
    readonly_fields = (
        "created",
    )
    list_editable = (
        "read",
        "admin_wrote",
    )

    def short_ticket(self, obj):
        if len(obj.ticket) > 40:
            return obj.ticket[:40] + "..."
        return obj.ticket

    short_ticket.short_description = "متن"

# ==========================
# Twit Admin
# ==========================
@admin.register(TwitModel)
class TwitAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "writer",
        "create_time",
    )
    search_fields = (
        "title",
        "description",
        "writer__username",
    )
    list_filter = (
        "create_time",
    )
    autocomplete_fields = (
        "writer",
    )
    readonly_fields = (
        "create_time",
    )

# ==========================
# Todo Admin
# ==========================
@admin.register(ToDoList2)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "short_description",
        "situation",
        "deadline1",
        "creat_time",
    )
    list_filter = (
        "situation",
        "creat_time",
    )
    search_fields = (
        "description",
        "user__username",
    )
    autocomplete_fields = (
        "user",
    )
    list_editable = (
        "situation",
    )

    def short_description(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + "..."
        return obj.description

    short_description.short_description = "توضیحات"

# ==========================
# Theme Admin
# ==========================
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "color1",
        "color2",
        "color3",
    )
    search_fields = (
        "user__username",
    )
    autocomplete_fields = (
        "user",
    )

# ==========================
# Text Admin
# ==========================
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = (
        "text_name",
        "s_description",
    )
    search_fields = (
        "text_name",
        "s_description",
    )

# ==========================
# Admin UI
# ==========================
admin.site.site_header = "Parham Social Admin"
admin.site.site_title = "Management Panel"
admin.site.index_title = "Site Control Center"
