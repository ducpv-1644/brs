from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


def user_directory_path(instance, filename):
    # Uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'user_{instance.user.id}/avatar/{filename}'

class User(AbstractBaseUser):
    ROLE_ADMIN = 1
    ROLE_MEMBER = 2
    USER_ROLES = (
        (ROLE_ADMIN, 'Sun Admin'),
        (ROLE_MEMBER, 'Sun Memeber'),
    )

    username = models.CharField(_('username'), max_length=150)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=ROLE_MEMBER)
    is_activate = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=user_directory_path, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return 'User: {}'.format(self.username)
