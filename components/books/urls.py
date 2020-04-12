from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookSearchView,
    BookCreateView,
    BookUpdateView,
    BookMarkReadView
)

app_name = 'book'

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('search/', BookSearchView.as_view(), name='book-search'),
    path('add/', BookCreateView.as_view(), name='book-create'),
    path('edit/<int:id>/', BookUpdateView.as_view(), name='book-update'),
    path('del/<int:id>/', BookUpdateView.as_view(), name='book-delete'),
    path('mark/<int:id>/', BookMarkReadView.as_view(), name='book-mark')
]