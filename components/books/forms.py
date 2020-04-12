from django import forms

from .models import Book


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'image', 'category']


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'image', 'category']


class BookMarkReadForm(forms.Form):
    page_reading = forms.IntegerField(min_value=1)
    is_favorite = forms.BooleanField(widget=forms.CheckboxInput)
    rating = forms.IntegerField()
