from datetime import datetime
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.postgres.search import SearchVector
from django.db.models.query import Q
from django.contrib import messages
from django.db.models import Avg

from components.users.decorators import admin_required
from .models import (
    Book, BookReadStatus, BookRequestBuy,
    BookReview, BookCategory
)
from .forms import (
    BookCreateForm, BookUpdateForm,
    BookMarkReadForm, BookFavoriteForm,
    BookRequestBuyForm, BookRequestBuyUpdateForm,
    BookReviewCreateForm, SearchBookForm, BookRatingCreateForm
)
from utility.log_activity import ActivityLog

logger = ActivityLog()


class BookListView(View):
    template_name = 'book_list.html'
    paginate_by = 25

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        query = Q(is_activate=True)

        books_favorite = []
        if request.GET.get('favorited') == 'true':
            books_favorite_qs = BookReadStatus.objects.filter(user=request.user,
                                                              is_favorite=True).values_list('book_id', flat=True)
            books_favorite.extend(list(books_favorite_qs))

        if request.GET.get('reading') == 'true':
            books_favorite_qs = BookReadStatus.objects.filter(user=request.user,
                                                              status=BookReadStatus.STATUS_CHOICES[1][0]
                                                              ).values_list('book_id', flat=True)
            books_favorite.extend(list(books_favorite_qs))

        if request.GET.get('read') == 'true':
            books_favorite_qs = BookReadStatus.objects.filter(user=request.user,
                                                              status=BookReadStatus.STATUS_CHOICES[2][0]
                                                              ).values_list('book_id', flat=True)
            books_favorite.extend(list(books_favorite_qs))

        if request.GET.get('favorited') == 'true' or request.GET.get('reading') == 'true' or request.GET.get(
                'read') == 'true':
            query = query & Q(id__in=list(set(books_favorite)))

        category = request.GET.get('category')
        if category:
            query = query & Q(book_category__name=category)

        books = Book.objects.filter(query).order_by('-updated_at')
        paginator = Paginator(books, self.paginate_by)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'books': page_obj})


class BookDetailView(View):
    template_name = 'book_detail.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(Book, pk=book_id)

        book_read_status_qs = BookReadStatus.objects.filter(book=book)
        book_reviews_qs = BookReview.objects.filter(book_id=book_id).first()
        rating = book_read_status_qs.aggregate(Avg('rating'))
        rating = round(rating['rating__avg']) if rating['rating__avg'] else 0
        context = {
            'id': book_id,
            'book': book,
            'rating': rating,
            'status': book_read_status_qs.filter(user=request.user).first(),
            'reviews': book_reviews_qs.messages if book_reviews_qs else [],
            'form_comment': kwargs.get('form_comment'),
            'form_bookmark': kwargs.get('form_bookmark'),
            'form_favorite': kwargs.get('form_favorite'),
            'form_rating': kwargs.get('form_rating')
        }
        return render(request, self.template_name, context)


class BookCategoryView(View):
    template_name = 'book_category.html'

    def get(self, request, *args, **kwargs):
        book_categories = BookCategory.objects.annotate(num_book=Count('book')).order_by('name')
        return render(request, self.template_name, {'categories': list(book_categories)})


class BookSearchView(View):
    template_name = 'book_list.html'
    form_class = SearchBookForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        search_form = self.form_class(request.POST)
        if search_form.is_valid():
            search_text = search_form.cleaned_data['q']
            books_qs = Book.objects.annotate(
                search=SearchVector(
                    'name', 'description', 'book_category__name'
                )
            ).filter(search=search_text).distinct('name')
            return render(request, self.template_name, {'books': books_qs, 'q': search_text})
        return redirect(reverse('book:book-list'))


class BookCreateView(View):
    template_name = 'book_create.html'
    form_class = BookCreateForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        categories = BookCategory.objects.all()
        context = {
            'categories': categories,
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        create_book_form = self.form_class(request.POST)
        if create_book_form.is_valid():
            item = create_book_form.save()
            return redirect(reverse('book:book-detail', kwargs={'id': item.id}))
        return render(request, self.template_name, {'form': create_book_form})


class BookUpdateView(View):
    template_name = 'book_update.html'
    form_class = BookUpdateForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        categories = BookCategory.objects.all()
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return render(request, '404.html', {'message': 'Book not found'})
        category_ids_selected = [item.id for item in book.book_category.all()]
        context = {
            'categories': categories,
            'category_ids_selected': category_ids_selected,
            'book': book,
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs.get('id'))
        update_book_form = self.form_class(request.POST, instance=book)
        if update_book_form.is_valid():
            book = Book.objects.filter(id=kwargs.get('id')).first()
            if not book:
                return render(request, '404.html', {'message': 'Book not found'})
            update_book_form.save()
            messages.success(request, 'Update book success!')
            return redirect(reverse('book:book-detail', kwargs={'id': kwargs.get('id')}))
        return render(request, self.template_name, {'form': update_book_form})


class BookDeleteView(View):

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        Book.objects.filter(id=book_id).update(is_activate=False)
        return redirect(reverse('book:book-list'))


class BookMarkReadView(BookDetailView):
    form_class = BookMarkReadForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs.get('id'))

        mark_read_form = self.form_class(request.POST)
        if mark_read_form.is_valid():
            page_reading = mark_read_form.cleaned_data['page_reading']
            book_read_status_qs = BookReadStatus.objects.filter(
                user=request.user,
                book=book
            ).first()
            if book_read_status_qs and page_reading == book.paperback:
                book_read_status_qs.page_reading = page_reading
                book_read_status_qs.status = BookReadStatus.STATUS_CHOICES[2][0]
                book_read_status_qs.save()
                logger.log_activity(source_user=request.user, obj_target=book, activity=logger.READ)
            elif book_read_status_qs and page_reading < book.paperback:
                book_read_status_qs.page_reading = page_reading
                book_read_status_qs.status = BookReadStatus.STATUS_CHOICES[1][0]
                book_read_status_qs.save()
                logger.log_activity(source_user=request.user, obj_target=book,
                                    activity=f'{logger.READING}-{page_reading}')
            elif not book_read_status_qs:
                book_read_status_qs = BookReadStatus.objects.create(
                    book=book,
                    status=BookReadStatus.STATUS_CHOICES[1][0],
                    page_reading=page_reading,
                )
                book_read_status_qs.user.add(request.user)
                logger.log_activity(source_user=request.user, obj_target=book,
                                    activity=f'{logger.READING}-{page_reading} page')

            return redirect(reverse('book:book-detail', kwargs={'id': kwargs.get('id')}))
        kwargs.update({'form_bookmark': mark_read_form})
        response = self.get(request, **kwargs)
        return response


class BookFavoriteView(BookDetailView):
    form_class = BookFavoriteForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs.get('id'))
        favorite_form = self.form_class(request.POST)
        if favorite_form.is_valid():
            is_favorite = favorite_form.cleaned_data['is_favorite']
            book_read_status_qs = BookReadStatus.objects.filter(
                user=request.user,
                book=book
            ).first()
            if book_read_status_qs:
                book_read_status_qs.is_favorite = is_favorite
                book_read_status_qs.save()
            else:
                book_read_status_qs = BookReadStatus.objects.create(
                    book=book,
                    is_favorite=True,
                    status=BookReadStatus.STATUS_CHOICES[0][0]
                )
                book_read_status_qs.user.add(request.user)
                book_read_status_qs.save()
            logger.log_activity(source_user=request.user, obj_target=book,
                                activity=logger.FAVORITE_MSG if is_favorite else logger.UNFAVORITE_MSG)
            return redirect(reverse('book:book-detail', kwargs={'id': kwargs.get('id')}))
        kwargs.update({'form_favorite': favorite_form})
        response = self.get(request, **kwargs)
        return response


class BookReviewCreateView(BookDetailView):
    form_class = BookReviewCreateForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')

        book_review_form = self.form_class(request.POST)
        if book_review_form.is_valid():
            book = Book.objects.get(id=book_id)
            book_review_qs = BookReview.objects.filter(book=book).first()

            now = datetime.now()
            if book_review_qs:
                book_messages_review = book_review_qs.messages
                book_messages_review.append(
                    [request.user.username,
                     book_review_form.cleaned_data['message'],
                     now.strftime("%m/%d/%Y, %H:%M:%S"),
                     str(request.user.id),
                     str(request.user.avatar.name)]
                )
                book_review_qs.messages = book_messages_review
                book_review_qs.save()
            else:
                book_review_qs = BookReview.objects.create(
                    book=book,
                    messages=[
                        [request.user.username,
                         book_review_form.cleaned_data['message'],
                         now.strftime("%m/%d/%Y, %H:%M:%S"),
                         str(request.user.id),
                         str(request.user.avatar.name)
                         ]]
                )
            logger.log_activity(source_user=request.user, obj_target=book_review_qs, activity=logger.COMMENT,
                                option_content=book_review_form.cleaned_data['message'])
            return redirect(reverse('book:book-detail', kwargs={'id': book_id}))
        kwargs.update({'form_comment': book_review_form})
        response = self.get(request, **kwargs)
        return response


class BookRatingCreateView(BookDetailView):
    form_class = BookRatingCreateForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        rating_form = self.form_class(request.POST)
        if rating_form.is_valid():
            book_read_status_qs = BookReadStatus.objects.filter(book__id=kwargs.get('id')).first()
            if book_read_status_qs:
                book_read_status_qs.rating = rating_form.cleaned_data['rating']
                book_read_status_qs.save()
            else:
                book_read_status_qs = BookReadStatus.objects.create(
                    book__id=kwargs.get('id'),
                    rating=rating_form.cleaned_data['rating']
                )
                book_read_status_qs.user.add(request.user)
                book_read_status_qs.save()
            return redirect(reverse('book:book-detail', kwargs={'id': kwargs.get('id')}))
        kwargs.update({'form_rating': rating_form})
        response = self.get(request, **kwargs)
        return response


class BookRequestBuyListView(View):
    template_name = 'book_list_request_buy.html'
    paginate_by = 25

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        books_requests_buy_qs = BookRequestBuy.objects.filter(is_activate=True).order_by('-updated_at')
        categories = BookCategory.objects.all()

        paginator = Paginator(books_requests_buy_qs, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'form_to_buy_book': kwargs.get('form_to_buy_book'),
            'form_update_request': kwargs.get('form_update_request'),
            'books_requests_buy': page_obj,
            'categories': categories
        }
        return render(request, self.template_name, context)


class BookRequestBuyCreateView(BookRequestBuyListView):
    template_name = 'book_create_request_buy.html'
    form_class = BookRequestBuyForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book_request_buy_form = self.form_class(request.POST)
        if book_request_buy_form.is_valid():
            request_book = BookRequestBuy.objects.create(
                book_url=book_request_buy_form.cleaned_data['book_url'],
                name=book_request_buy_form.cleaned_data['name'],
                price=book_request_buy_form.cleaned_data['price'],
                user=request.user
            )
            request_book.book_category.set(book_request_buy_form.cleaned_data['book_category'])
            request_book.save()

            return redirect(reverse('book:list-request-buy'))
        kwargs.update({'form_to_buy_book': book_request_buy_form})
        response = self.get(request, **kwargs)
        return response


class BookRequestBuyUpdateView(BookRequestBuyListView):
    form_class = BookRequestBuyUpdateForm

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        book_request_buy_id = kwargs.get('id')
        book_request_buy_update_form = self.form_class(request.POST)
        if book_request_buy_update_form.is_valid():
            book_request_buy_qs = BookRequestBuy.objects.filter(id=book_request_buy_id).first()
            if not book_request_buy_qs:
                return render(request, '404.html', {'message': 'Request book not found'})
            book_request_buy_qs.status = book_request_buy_update_form.cleaned_data['status']
            book_request_buy_qs.save()

            return redirect(reverse('book:list-request-buy'))
        kwargs.update({'form_update_request': book_request_buy_update_form})
        response = self.get(request, **kwargs)
        return response
