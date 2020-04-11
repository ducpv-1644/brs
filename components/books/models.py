from django.db import models


class BookCategory(models.Model):
    name = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=256, null=False)
    description = models.TextField()
    image = models.URLField(null=False)
    category = models.ManyToManyField(BookCategory)

    def __str__(self):
        return self.name