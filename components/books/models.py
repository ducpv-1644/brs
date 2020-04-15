from django.db import models
from django.contrib.postgres.fields import ArrayField

from components.users.models import User


class BookCategory(models.Model):
    name = models.CharField(max_length=128, null=False)

    class Meta:
        db_table = 'book_category'

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=256, null=False)
    description = models.TextField()
    image = models.URLField(null=False)
    book_category = models.ManyToManyField(BookCategory)
    paperback = models.IntegerField(default=1)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.name


class BookReadStatus(models.Model):
    STATUS_CHOICES = (
        ('0', 'unread'),
        ('1', 'reading'),
        ('2', 'read'),
    )

    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    status = models.CharField(choices=STATUS_CHOICES, default='0', max_length=56)
    page_reading = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        db_table = 'book_read_status'

    def __str(self):
        return self.page_reading


class BookRequestBuy(models.Model):
    STATUS_CHOICES = (
        (1, 'waiting'),
        (2, 'approved'),
        (3, 'bought'),
        (4, 'reject')
    )
    book_category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    book_url = models.URLField()
    name = models.CharField(max_length=256)
    price = models.IntegerField(default=1)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_request_buy'

    def __str__(self):
        return self.book_url


class BookReview(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    messages = ArrayField(ArrayField(models.CharField(max_length=512, blank=True)))

    class Meta:
        db_table = 'book_review'

    def __str__(self):
        return self.book.name
