from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


def user_directory_path(instance, filename):
    # Uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'user_{instance.id}/avatar/{filename}'


class UserBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, UserBase):
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
    education = models.CharField(max_length=256, null=True)
    location = models.CharField(max_length=256, null=True)
    skills = models.CharField(max_length=256, null=True)
    notes = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return 'User: {}'.format(self.username)


class UserFollow(UserBase):
    STATUS_FOLLOW = (
        (1, 'unfollow'),
        (2, 'follow')
    )
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, null=True)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null=True)
    status = models.IntegerField(choices=STATUS_FOLLOW, default=1)

    class Meta:
        db_table = 'user_follow'
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
