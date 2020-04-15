from django.db import models
from django.contrib.postgres.fields import ArrayField

from components.users.models import User


class BookBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BookCategory(models.Model):
    name = models.CharField(max_length=128, null=False)

    class Meta:
        db_table = 'book_category'

    def __str__(self):
        return self.name


class Book(BookBase):
    LANGUAGE_CHOICES = (
        (0, 'VN'),
        (1, 'JP'),
        (2, 'EN'),
    )

    name = models.CharField(max_length=256, null=False)
    description = models.TextField()
    image = models.URLField(null=False, blank=True)
    book_category = models.ManyToManyField(BookCategory)
    author = models.CharField(max_length=128, null=True, blank=True)
    paperback = models.IntegerField(default=1)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=0)
    publisher = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.name


class BookReadStatus(BookBase):
    STATUS_CHOICES = (
        (0, 'unread'),
        (1, 'reading'),
        (2, 'read'),
    )

    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    page_reading = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        db_table = 'book_read_status'

    def __str(self):
        return self.page_reading


class BookRequestBuy(BookBase):
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


class BookReview(BookBase):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    messages = ArrayField(ArrayField(models.CharField(max_length=512, blank=True)))

    class Meta:
        db_table = 'book_review'

    def __str__(self):
        return self.book.name
