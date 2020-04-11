from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.postgres.search import SearchVector, SearchQuery


from .models import Book
from .forms import BookCreateForm, BookUpdateForm

class BookListView(View):

    template_name = 'list_book.html'

    def get(self, request, *args, **kwargs):
        books_qs = Book.objects.all()
        return render(request, self.template_name, {'books': books_qs})


class BookDetailView(View):

    template_name = 'detail_book.html'

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(Book, pk=book_id)
        return render(request, self.template_name, {'book': book})


class BookSearchView(View):

    template_name = 'list_book.html'

    def get(self, request, *args, **kwargs):
        search_text = request.GET.get('q')
        books_qs = Book.objects.annotate(
            search=SearchVector(
                'name', 'description','category__name'
            )
        ).filter(search=search_text).distinct('name')

        return render(request, self.template_name, {'books': books_qs})


class BookCreateView(View):

    template_name = 'create_book.html'
    form_class = BookCreateForm
    success_url = '/book/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        create_book_form = self.form_class(request.POST)
        if create_book_form.is_valid():
            create_book_form.save()
            return redirect(self.success_url)


class BookUpdateView(View):

    template_name = 'update_book.html'
    form_class = BookUpdateForm
    success_url = '/book/'

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book_qs = get_object_or_404(Book, pk=book_id)
        update_book_form = self.form_class(instance=book_qs)
        return render(request, self.template_name, {'form': update_book_form, 'id': book_id})

    def put(self, request, *args, **kwargs):
        update_book_form = self.form_class(request.PUT)
        if update_book_form.is_valid():
            update_book_form.save()


class BookDeleteView(View):

    success_url = '/book/'

    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book_qs = get_object_or_404(Book, pk=book_id)
        book_qs.delete()
        return redirect(self.success_url)
