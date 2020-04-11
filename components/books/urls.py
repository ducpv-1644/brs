from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookSearchView,
    BookCreateView,
    BookUpdateView
)

app_name = 'book'

urlpatterns = [
    path('', BookListView.as_view(), name='list-book'),
    path('<int:id>/', BookDetailView.as_view(), name='detail-book'),
    path('search/', BookSearchView.as_view(), name='search-book'),
    path('add/', BookCreateView.as_view(), name='create-book'),
    path('edit/<int:id>/', BookUpdateView.as_view(), name='update-book'),
    path('del/<int:id>/', BookUpdateView.as_view(), name='delete-book'),
]