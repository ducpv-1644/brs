from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookSearchView,
    BookCreateView,
    BookUpdateView,
    BookMarkReadView,
    BookFavoriteView,
    BookRequestBuyCreateView,
    BookRequestBuyListView,
    BookRequestBuyUpdateView,
    BookReviewCreateView,
    index
)

app_name = 'book'

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('search/', BookSearchView.as_view(), name='book-search'),
    path('add/', BookCreateView.as_view(), name='book-create'),
    path('edit/<int:id>/', BookUpdateView.as_view(), name='book-update'),
    path('del/<int:id>/', BookUpdateView.as_view(), name='book-delete'),
    path('mark/<int:id>/', BookMarkReadView.as_view(), name='book-mark'),
    path('like/<int:id>', BookFavoriteView.as_view(), name='book-like'),
    path('add-request-buy/', BookRequestBuyCreateView.as_view(), name='add-request-buy'),
    path('list-request-buy/', BookRequestBuyListView.as_view(), name='list-request-buy'),
    path('edit-request-buy/<int:id>', BookRequestBuyUpdateView.as_view(), name='edit-request-buy'),
    path('review/<int:id>', BookReviewCreateView.as_view(), name='book-review'),
    path('test', index)
]