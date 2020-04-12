from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.postgres.search import SearchVector

from components.accounts.decorators import admin_required
from components.accounts.models import Account
from .models import (
    Book, BookReadStatus
)
from .forms import (
    BookCreateForm, BookUpdateForm,
    BookMarkReadForm
)


class BookListView(View):
    template_name = 'book_list.html'

    def get(self, request, *args, **kwargs):
        books_qs = Book.objects.all()
        return render(request, self.template_name, {'books': books_qs})


class BookDetailView(View):
    template_name = 'book_detail.html'

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(Book, pk=book_id)

        book_read_status_qs = None
        if request.user:
            book_read_status_qs = BookReadStatus.objects.filter(
                book=book,
                account__user=request.user
            ).first()

        context = {
            'id': book_id,
            'book': book,
            'status': book_read_status_qs
        }
        return render(request, self.template_name, context)


class BookSearchView(View):
    template_name = 'book_list.html'

    def get(self, request, *args, **kwargs):
        search_text = request.GET.get('q')
        books_qs = Book.objects.annotate(
            search=SearchVector(
                'name', 'description', 'category__name'
            )
        ).filter(search=search_text).distinct('name')

        return render(request, self.template_name, {'books': books_qs})


class BookCreateView(View):
    template_name = 'book_create.html'
    form_class = BookCreateForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        create_book_form = self.form_class(request.POST)
        if create_book_form.is_valid():
            item = create_book_form.save()
            return redirect(reverse('book:book-detail', kwargs={'id': item.id}))


class BookUpdateView(View):
    template_name = 'book_update.html'
    form_class = BookUpdateForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book_qs = get_object_or_404(Book, pk=book_id)
        update_book_form = self.form_class(instance=book_qs)
        return render(request, self.template_name, {'form': update_book_form, 'id': book_id})

    @method_decorator(admin_required)
    def put(self, request, *args, **kwargs):
        update_book_form = self.form_class(request.PUT)
        if update_book_form.is_valid():
            update_book_form.save()

            return redirect(reverse('book-detail'))


class BookDeleteView(View):

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book_qs = get_object_or_404(Book, pk=book_id)
        book_qs.delete()
        return redirect(reverse('book-list'))


class BookMarkReadView(View):
    template_name = 'book_detail.html'
    form_class = BookMarkReadForm

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs.get('id'))
        account = Account.objects.get(user=request.user)

        mark_read_form = self.form_class(request.POST)
        if mark_read_form.is_valid():
            page_reading = mark_read_form.cleaned_data['page_reading']
            book_read_status_qs = BookReadStatus.objects.filter(
                account=account,
                book=book
            ).first()
            if book_read_status_qs and page_reading == book.paperback:
                book_read_status_qs.page_reading = page_reading
                book_read_status_qs.status = BookReadStatus.STATUS_CHOICES[2][0]
                book_read_status_qs.save()
            elif book_read_status_qs and page_reading < book.paperback:
                book_read_status_qs.page_reading = page_reading
                book_read_status_qs.status = BookReadStatus.STATUS_CHOICES[1][0]
                book_read_status_qs.save()
            elif not book_read_status_qs:
                book_read_status_qs = BookReadStatus.objects.create(
                    book=book,
                    status=BookReadStatus.STATUS_CHOICES[1][0],
                    page_reading=page_reading
                )
                book_read_status_qs.account.add(account)
            return redirect(reverse('book:book-detail', kwargs={'id': kwargs.get('id')}))
