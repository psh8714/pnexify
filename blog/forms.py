from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, inlineformset_factory

from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(required=True)
    email = forms.EmailField()
    phone = forms.CharField(required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, widget=forms.Select(attrs={"id":"subject_select"}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره باید عدد باشد")
            elif len(phone) != 11:
                raise forms.ValidationError("شماره باید یازده رقمی باشد")
            else:
                return phone


class LTicket(forms.ModelForm):
    class Meta:
        model = LocalTicket
        fields = ['ticket']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['name', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()


class NewPost(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'tags', 'reading_time']

        widgets = {
            "category": forms.Select(
                attrs={
                    "id": "category-select"
                }
            ),
            "tags": forms.SelectMultiple(),
            "title": forms.TextInput(attrs={'style':'direction: rtl;unicode-bidi: plaintext;text-align: right;'}),
        }


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePost
        fields = ['image_file']


ImageFormSet = inlineformset_factory(
    Post,
    ImagePost,
    form=ImagePostForm,
    fields=['image_file'],
    extra=1,
    can_delete=True,
)


class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        fields = [
            'project_url',
            'github_url',
            'status'
        ]

        widgets = {
            "status": forms.Select(
                attrs={
                    "id": "status-select"
                }
            ),
            "github_url": forms.URLInput(
                attrs={'placeholder': 'example: http://github/.../project1'}
            ),
            "project_url": forms.URLInput(
                attrs={
                    'placeholder': 'example: http://pnexify.ir',
                }
            )
        }


class TwitForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'موضوع'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'فکر بزرگ تو'}))

    class Meta:
        model = TwitModel
        fields = ['title', 'description']


# class LoginForm(forms.Form):
#     name = forms.CharField(max_length=250, required=True, label='username')
#     password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250, label='password')
class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True, label='نام کاربری/شماره/ایمیل')
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput, label='گذرواژه')

    # class Meta:
    #     model = User
    #     fields = ['username', 'password']
    #
    # def clean_username(self):
    #     user_name = self.cleaned_data['username']
    #     if User.objects.filter(username=user_name).exists():
    #         return user_name
    #     else:
    #         raise ValidationError('user name is undefined')
    # ---------------
    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            if User.objects.get(username=username).check_password(password):
                return cleaned_data
            else:
                raise ValidationError('enter correct password')
        elif User.objects.filter(phone_number=username).exists():
            if User.objects.get(phone_number=username).check_password(password):
                return cleaned_data
            else:
                raise ValidationError('enter correct password')

        elif User.objects.filter(email=username).exists():
            if User.objects.get(email=username).check_password(password):
                return cleaned_data
            else:
                raise ValidationError('enter correct password')
        else:
            raise ValidationError('user is undefined')


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password']:
            raise ValidationError('passwords not match')
        elif len(self.cleaned_data['password']) < 4:
            raise ValidationError('password should be longer than 3 character')
        return self.cleaned_data['password2']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise ValidationError('this username already exist')
        else:
            return self.cleaned_data['username']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'photo', 'ostan', 'city', 'github_id', 'bio',
                  'tel_id', 'main_skill', 'date_of_birth', 'level']

        widgets = {
            "ostan": forms.Select(
                attrs={'id': 'ostan_select'}
            ),
            "date_of_birth": forms.DateInput(
                attrs={'placeholder': 'example: 1387-4-5'}
            ),

            "tel_id": forms.TextInput(
                attrs={'placeholder': 'example: parham_sh8721'}
            ),
            "username": forms.TextInput(
                attrs={'placeholder': 'your unique nickname'}
            ),
            "github_id": forms.TextInput(
                attrs={'placeholder': 'example: psh8714'}
            ),
            "main_skill": forms.TextInput(
                attrs={'placeholder': 'a programing language(english name)'}
            ),
            "level": forms.Select(
                attrs={'placeholder': 'your level', 'id':'user_level_select'}
            ),
            "phone_number": forms.TextInput(
                attrs={'placeholder': 'شماره'}
            ),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill', 'level']

        widgets = {
            "level": forms.Select(
                attrs={'id': 'level_select'}
            )
        }


SkillFormSet = modelformset_factory(
    Skill,
    form=SkillForm,
    can_delete=True,
    extra=1
)


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList2
        fields = ['description', 'deadline1']
