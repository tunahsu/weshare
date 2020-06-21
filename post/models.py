from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

from sorl.thumbnail import ImageField


class Post(models.Model):
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    image = ImageField(upload_to='images/%Y/%m/%d/')
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='post_created'
    )
    user_like = models.ManyToManyField(
        to=User,
        related_name='posts_liked',
        blank=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Post {} by {}'.format(self.body, self.user.first_name)
    

class Comment(models.Model):
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments_created'
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user.first_name)
    