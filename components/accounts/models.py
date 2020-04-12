from django.contrib.auth.models import User
from django.db import models



class Account(models.Model):
    ROLE_CHOICES = (
        ('1', 'normal'),
        ('0', 'admin')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField()
    role = models.CharField(choices=ROLE_CHOICES, default='1', max_length=128)

    def __str__(self):
        return self.user.username
