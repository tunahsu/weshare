from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

from sorl.thumbnail import ImageField


class Image(models.Model):
    # title = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    image = ImageField(upload_to='images/%Y/%m/%d/')
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='images_created'
    )
    user_like = models.ManyToManyField(
        to=User,
        related_name='images_liked',
        blank=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.description

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Image, self).save(*args, **kwargs)
    
