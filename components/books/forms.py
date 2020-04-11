from django.forms import ModelForm

from .models import Book


class BookCreateForm(ModelForm):

    class Meta:
        model = Book
        fields = ['name', 'description', 'image', 'category']


class BookUpdateForm(ModelForm):

    class Meta:
        model = Book
        fields = ['name', 'description', 'image', 'category']