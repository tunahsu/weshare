from django.db import models
from django.contrib.auth.models import User

from hashlib import md5
from sorl.thumbnail import ImageField, get_thumbnail


class Contact(models.Model):
    user_from = models.ForeignKey(
        to=User,
        related_name='from_set',
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        to=User,
        related_name='to_set',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

User.add_to_class(
    'following',
    models.ManyToManyField(
        to=User,
        through=Contact,
        through_fields=('user_from', 'user_to'),
        related_name='followers',
        symmetrical=False
    )
)

User.add_to_class(
    'about',
    models.TextField(blank=True)
)

User.add_to_class(
    'avatar',
    ImageField(upload_to='avatars/%Y/%m/%d/', blank=True)
)

def get_avatar(self, size=150):
    if self.avatar:
        avatar_url = get_thumbnail(self.avatar, '150x150', crop='center', quality=99).url
    else:
        md5_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        avatar_url= 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(md5_digest, size)
    return avatar_url


User.add_to_class(
    'get_avatar',
    get_avatar
)
