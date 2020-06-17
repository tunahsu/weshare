from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from account import views
from account.forms import MyAuthenticationForm, MyPasswordChangeForm

app_name = 'account'
urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='account/login.html',
            authentication_form=MyAuthenticationForm
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'register/',
        views.register,
        name='register'
    ),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy('account:password_change_done'),
            template_name='account/password_change.html',
            form_class=MyPasswordChangeForm
            ),
        name='password_change'
    ),
    path(
        'password-change-done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
        name='password_change_done'
    ),
    path(
        'user/<str:username>/',
        views.user_profile,
        name='user_profile'
    ),
    path(
        'edit/',
        views.user_edit,
        name='user_edit'
    ),
    path(
        'user/follow/<str:username>/',
        views.user_follow,
        name='user_follow'
    ),
    path(
        'user/unfollow/<str:username>/',
        views.user_unfollow,
        name='user_unfollow'
    ),
]