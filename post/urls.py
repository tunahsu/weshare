from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from post import views

app_name = 'post'
urlpatterns = [
    path(
        'post/upload/',
        views.post_upload,
        name='post_upload'
    ),
    path(
        '',
        views.post_list,
        name='post_list'
    ),
    path(
        'post/detail/<int:id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'post/like/',
        views.post_like,
        name='post_like'
    ),
    path(
        'post/',
        views.get_post,
        name='get_post'
    ),
    path(
        'post/comment',
        views.comment,
        name='comment'
    )
]
