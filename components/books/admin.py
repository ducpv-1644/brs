from django.contrib import admin

from components.books.models import Book, BookCategory

admin.site.register(Book)
admin.site.register(BookCategory)