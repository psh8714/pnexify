from pickletools import optimize
from random import choices
from tkinter.constants import CASCADE

from django.db import models
from django.db.models import OneToOneRel, OneToOneField
from django.db.models.fields import TextField, EmailField, CharField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import datetime

from django_resized import ResizedImageField
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Province(models.TextChoices):
    AZARBAIJAN_SHARGHI = "azarbaijan_sharghi", "آذربایجان شرقی"
    AZARBAIJAN_GHARBI = "azarbaijan_gharbi", "آذربایجان غربی"
    ARDABIL = "ardabil", "اردبیل"
    ESFAHAN = "esfahan", "اصفهان"
    ALBORZ = "alborz", "البرز"
    ILAM = "ilam", "ایلام"
    BUSHEHR = "bushehr", "بوشهر"
    TEHRAN = "tehran", "تهران"
    CHAHARMAHAL_BAKHTIARI = "chaharmahal_bakhtiari", "چهارمحال و بختیاری"
    KHORASAN_JONOOBI = "khorasan_jonoobi", "خراسان جنوبی"
    KHORASAN_RAZAVI = "khorasan_razavi", "خراسان رضوی"
    KHORASAN_SHOMALI = "khorasan_shomali", "خراسان شمالی"
    KHUZESTAN = "khuzestan", "خوزستان"
    ZANJAN = "zanjan", "زنجان"
    SEMNAN = "semnan", "سمنان"
    SISTAN_BALUCHESTAN = "sistan_baluchestan", "سیستان و بلوچستان"
    FARS = "fars", "فارس"
    QAZVIN = "qazvin", "قزوین"
    QOM = "qom", "قم"
    KORDESTAN = "kordestan", "کردستان"
    KERMAN = "kerman", "کرمان"
    KERMANSHAH = "kermanshah", "کرمانشاه"
    KOHGILUYEH_BOYERAHMAD = "kohgiluyeh_boyerahmad", "کهگیلویه و بویراحمد"
    GOLESTAN = "golestan", "گلستان"
    GILAN = "gilan", "گیلان"
    LORESTAN = "lorestan", "لرستان"
    MAZANDARAN = "mazandaran", "مازندران"
    MARKAZI = "markazi", "مرکزی"
    HORMOZGAN = "hormozgan", "هرمزگان"
    HAMADAN = "hamadan", "همدان"
    YAZD = "yazd", "یزد"


class User(AbstractUser):
    LEVEL_CHOICES = (
        ('beginner', '(junior)مبتدی'),
        ('middle', '(mid-level)متوسط'),
        ('professional', '(senior)حرفه ای'),
    )
    photo = models.ImageField(upload_to='blog/static/images/profile/', blank=True, null=True)
    ostan = models.CharField(verbose_name='استان', max_length=50, choices=Province.choices, blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='شهر', blank=True, null=True)
    phone_number = models.CharField(max_length=13, verbose_name='phone', null=True, blank=True)
    bio = models.TextField(max_length=250, verbose_name='bio', null=True, blank=True)
    tel_id = models.CharField(max_length=50, verbose_name='telegram_id', null=True, blank=True)
    github_id = models.CharField(max_length=500, verbose_name='github_id', null=True, blank=True)
    main_skill = models.CharField(max_length=40, verbose_name='main_skill', null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='birth_day', null=True, blank=True)
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    saved_posts = models.ManyToManyField('Post', related_name='saver_accounts', blank=True)
    notif = models.CharField(blank=True)
    verify = models.BooleanField(default=False)
    level = models.CharField(choices=LEVEL_CHOICES, verbose_name='سطح', default='beginner')
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'


# class Portfolio(models.Model):
#     user = models.ForeignKey(User, related_name='portfolios', on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     project_url = models.URLField(
#         blank=True
#     )
#     github_url = models.URLField(
#         blank=True
#     )
#     portfolio = models.TextField(verbose_name='پروژه و نمونه کار(حتی کوچیک)')
#     image1 = models.ImageField(verbose_name='تصویر اول', null=True, blank=True, upload_to='portfolio/')
#     image2 = models.ImageField(verbose_name='تصویر دوم', null=True, blank=True, upload_to='portfolio/')
#     image3 = models.ImageField(verbose_name='تصویر سوم', null=True, blank=True, upload_to='portfolio/')


class Skill(models.Model):
    LEVEL_CHOICES = (
        ('beginner', '(junior)مبتدی'),
        ('middle', '(mid-level)متوسط'),
        ('professional', '(senior)حرفه ای'),
    )
    user = models.ForeignKey(User, related_name='abilities', on_delete=models.CASCADE)
    skill = models.CharField(max_length=250, verbose_name='مهارت', blank=True)
    level = models.CharField(choices=LEVEL_CHOICES, verbose_name='سطح', default='beginner')

    confirmed = models.BooleanField(default=False, verbose_name='تایید شده بودن')


class Tag(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'در حال بررسی'
        PUBLISHED = 'PB', 'منتشر شده'
        REJECTED = 'RJ', 'رد شده'

    CATEGORY_CHOICES = (
        ('WIL', 'چیزی که یاد گرفتم'),
        ('WIC', 'پروزه یا نمونه کار ساختم'),
        ('SFT', 'دتبال هم تیمی میگزدم'),
        ('IHQ', 'سوال درام')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default='WIL')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    total_saves = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    reading_time = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']

        indexes = [
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])


class Technology(models.Model):
    name = models.CharField(max_length=50, verbose_name='تکنولوژی', default='___')


class ProjectDetail(models.Model):
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        related_name='project_detail'
    )
    technologies = models.ManyToManyField(Technology, blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("completed", "تکمیل شده"),
            ("ongoing", "در حال توسعه"),
        ]
    )


class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='post')
    name = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    helpful = models.BooleanField(default=False)



    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"{self.name} commented on {self.post}"


from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from pathlib import Path


class ImagePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='post')
    title = models.CharField(null=True, blank=True)
    description = models.CharField(null=True, blank=True)

    def image_directory(self, filename):
        return datetime.now().strftime("%Y/%m/%d/") + filename

    image_file = models.ImageField(upload_to=image_directory)

    def save(self, *args, **kwargs):
        if self.image_file:
            print("قبل از پردازش:", self.image_file.size / 1024, "KB")
            print(self.image_file)
            print(type(self.image_file))

            # تبدیل به یک ابجکت PIL.Image.Image که میتونیم بعد از این هر تغییری روش اعمال کنیم
            img = Image.open(self.image_file)

            # ثابت کردن فرمت رنگ عکس
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            max_width = 1200

            # مثال: 1200/6000 - > 0.2 ---> height * 0.2 ---> بیست درصد اندازه اولیه
            if img.width > max_width:
                ratio = max_width / img.width

                new_height = int(img.height * ratio)

                img = img.resize(
                    (max_width, new_height),
                    # LANCZOS بهترین الگوریتم کوچک کردن عکس
                    Image.Resampling.LANCZOS
                )

            # یک فایل روی رم میسازد نه روی هارد
            buffer = BytesIO()

            # ذخیره ی عکس روی رم(داخل بافر)
            img.save(
                buffer,
                format="WEBP",
                quality=80,
                # optimize باعث میشود pillow کمی زمان بیشتری مصرف کند ولی حجم فایل کمتر میشود
                optimize=True
            )

            # بازگست اساره گر خوندن فایل به اول صفحع
            buffer.seek(0)

            # فایل بدون format.
            filename = Path(self.image_file.name).stem

            self.image_file.save(
                f"{filename}.webp",
                # داده های توی رم را میخواند و تبدیل به فایل قابل ذخیره برای جنگو میکند
                ContentFile(buffer.read()),
                # جلوگیری از ایجاد حلقه صدا زدن save
                save=False
            )

        super().save(*args, **kwargs)

        print(self.image_file.size / 1024, "KB")

    # image_file = models.ImageField(upload_to=image_directory)-----------------------


class TwitModel(models.Model):
    title = models.CharField(max_length=250, verbose_name="title")
    description = models.TextField(verbose_name="description", max_length=1500)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['create_time']
        indexes = [
            models.Index(fields=['create_time'])
        ]

    def __str__(self):
        return self.title


class ToDoList2(models.Model):
    description = models.TextField(verbose_name='description')
    situation = models.BooleanField(verbose_name='situation', default=False)
    deadline1 = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_do_list', verbose_name='user')
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name='creat_time')


class LocalTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tickets', verbose_name='user')
    ticket = models.TextField(verbose_name="text", max_length=1500)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created_time')
    read = models.BooleanField(default=False)
    admin_wrote = models.BooleanField(default=False)


class Text(models.Model):
    s_description = models.CharField()
    text_name = models.CharField(unique=True)


class Theme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='theme')
    color1 = models.CharField(max_length=7)
    color2 = models.CharField(max_length=7)
    color3 = models.CharField(max_length=7)
    color4 = models.CharField(max_length=7)
    color5 = models.CharField(max_length=7)
    color6 = models.CharField(max_length=7)


class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TeamMember(models.Model):
    ROLES = (
    ("leader",  "رهبر" ),
    ("normal",  "عضو" ),
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, max_length=30, default="normal")

    class Meta:
        unique_together = ("team", "user")


class TeamRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_team_requests"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)