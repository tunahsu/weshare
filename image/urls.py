from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from image import views

app_name = 'image'
urlpatterns = [
    path(
        'image/upload/',
        views.image_upload,
        name='image_upload'
    ),
    path(
        '',
        views.image_list,
        name='image_list'
    ),
    path(
        'image/like/',
        views.image_like,
        name='image_like'
    ),
    path(
        'image/',
        views.get_image,
        name='get_image'
    )
]
