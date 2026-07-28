from django.contrib import admin
from django.core.mail import send_mail

from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

def email_sender_publisher(modeadnim, request, queryset):
    queryset.update(status=Post.Status.PUBLISHED)
    for post in queryset:
        message = f"hi \n {post.title} checked and published by admin"
        send_mail("your post Published", message, "parham.nadim7777@gmail.com", [post.author.email])
    modeadnim.message_user(request, 'successful action')


email_sender_publisher.short_description = 'انتشار پست'


def email_sender_rejecter(modeadnim, request, queryset):
    queryset.update(status=Post.Status.REJECTED)
    for post in queryset:
        message = f"hi \n {post.title} checked and rejected by admin"
        send_mail("your post Rejected", message, "parham.nadim7777@gmail.com", [post.author.email])
    modeadnim.message_user(request, 'successful action')


email_sender_rejecter.short_description = 'رد انتشار پست'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'author_id', 'slug', 'status', 'publish',)
    ordering = ('-publish',)
    search_fields = ('title', 'slug')
    list_filter = ('status', 'author')
    fieldsets = (
        ("اطلاعات اجباری", {
            "fields": ("title", "author", "description"),
        }),
        ("تنظیمات پیشرفته", {
            "classes": ("collapse",),
            "fields": ("slug", "publish", "status", "category", 'total_likes', 'total_saves'),
        }),
    )
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    list_per_page = 10
    list_editable = ('status',)
    list_display_links = ('title',)
    actions = [email_sender_publisher, email_sender_rejecter]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'active', 'helpful', 'post', 'created']
    list_filter = ['name', 'active']
    list_editable = ['active','helpful']
    search_fields = ['name', 'body', 'post__title']


@admin.register(TwitModel)
class TwitModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'writer', 'create_time', 'description']


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone_number', 'notif']
    fieldsets = UserAdmin.fieldsets + ((
                                           'Additional Info', {
                                           'fields': ('date_of_birth', 'city', 'phone_number', 'bio', 'tel_id', 'github_id', 'main_skill',
                                                      'photo', 'followings', 'notif', 'verify', 'ostan')}
                                       ),)


@admin.register(ToDoList2)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'deadline1']


@admin.register(ImagePost)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'image_file']


@admin.register(LocalTicket)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'admin_wrote']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'level', 'confirmed']


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['text_name', 's_description']

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(ProjectDetail)
class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = ['post']