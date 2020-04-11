from django.urls import path

from .views import (
    # BookListView,
    # BookDetailView,
    # BookSearchView,
    # BookCreateView,
    # BookUpdateView
    SignUpView
)

app_name = 'account'

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    # path('<int:id>/', BookDetailView.as_view(), name='detail-book'),
    # path('search/', BookSearchView.as_view(), name='search-book'),
    # path('add/', BookCreateView.as_view(), name='create-book'),
    # path('edit/<int:id>/', BookUpdateView.as_view(), name='update-book'),
    # path('del/<int:id>/', BookUpdateView.as_view(), name='delete-book'),
]