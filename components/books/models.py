from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from components.accounts.models import Account


class BookCategory(models.Model):
    name = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=256, null=False)
    description = models.TextField()
    image = models.URLField(null=False)
    category = models.ManyToManyField(BookCategory)
    paperback = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class BookReadStatus(models.Model):
    STATUS_CHOICES = (
        ('0', 'unread'),
        ('1', 'reading'),
        ('2', 'read'),
    )

    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    account = models.ManyToManyField(Account)
    status = models.CharField(choices=STATUS_CHOICES, default='0', max_length=56)
    page_reading = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)

    def __str(self):
        return self.page_reading


class BookRequestBuy(models.Model):
    STATUS_CHOICES = (
        ('0', 'waiting'),
        ('1', 'approved'),
        ('2', 'bought'),
        ('3', 'reject')
    )
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    book_url = models.URLField()
    name = models.CharField(max_length=256)
    price = models.IntegerField(default=1)
    status = models.CharField(choices=STATUS_CHOICES, default='0', max_length=56)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_url
