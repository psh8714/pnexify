from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/category/<str:category>', views.post_list, name='post_list_category'),
    path('posts/<slug:slug>', views.post_detail, name='post_detail'),

    # path('post/<post_slug>/comment', views.comment_view, name='post_comment'),
    path('post/comment', views.comment, name='post_comment'),
    path('index/contact', views.ticket_view, name='ticket'),
    path('index/contact/local', views.l_ticket_view, name='local_ticket'),
    path('index/contact/local/<user_id>', views.l_ticket_view, name='local_ticket_admin'),
    path('index/contact/local_ticket_admin', views.l_ticket_admin_view, name='local_tickets_admin'),
    path('index/about-us', views.about_us_view, name='about_us'),
    path('index/search', views.search_view, name='search_view'),
    path('index/profile', views.profile_view, name='profile_view'),
    path('index/addpost', views.new_post_view, name='new_post_view'),
    path('index/editpost/<post_slug>', views.edit_post, name='edit_post_view'),
    path('index/deletepost/<post_slug>', views.delete_post, name='delete_post_view'),
    path('index/free_twit', views.twit_view, name='twit_view'),
    path('index/delete_twit<twit_id>', views.delete_twit, name='delete_twit_view'),
    # path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='logout'),
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', views.login_, name='login'),
    path('password-change/', PasswordChangeView.as_view(success_url='done/'), name='change_password'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='change_password_done'),
    path('reset-password/', PasswordResetView.as_view(success_url='done/'), name='reset_password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset-password/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(success_url='/blog/reset-password/complete'), name='reset_password_confirm'),
    path('reset-password/complete', PasswordResetCompleteView.as_view(), name='reset_password_complete'),
    path('user/register', views.user_register, name='user_register'),
    path('edit/user/', views.user_edit, name='user_edit'),
    path('index/to-do-list', views.to_do_list, name='to_do_list'),
    path('index/to-do-list/<int:pk>/<bol>', views.to_do_list, name='to_do_list_change'),
    path('index/delete-to-do-list/<task_id>', views.delete_to_do_list, name='to_do_list_delete'),
    path('index/lr', views.login_or_register, name='register_or_login'),
    path('post_like/', views.post_like, name='post_like'),
    path('follow_user/', views.follow_user, name='user_follow'),
    path('save_post/', views.save_post, name='save_post'),
    path('users/', views.user_list, name='user_list'),
    path('users/<user_id>/<is_follow>', views.user_list, name='follow_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('download/image/<int:pk>/', views.download_image, name='image_download'),
    path('header/color', views.header_color, name='header_color'),
    path('theme/apply/', views.header_color_success, name='header_color_success'),
    path('team/request', views.ticket_view, name='team_make')

]
