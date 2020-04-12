from django.urls import path

from .views import (
    # BookListView,
    AccountDetailView,
    AccountSearchView,
    AccountDeleteView,
    AccountUpdateView,
    SignUpView,
    SignInView,
    SignOutView,
    AccountListView,
    ChangeRoleAccountView
)

app_name = 'account'

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('signin', SignInView.as_view(), name='signin'),
    path('signout', SignOutView.as_view(), name='signout'),
    path('change-role', ChangeRoleAccountView.as_view(), name='change-role'),

    path('', AccountListView.as_view(), name='account-list'),
    path('search/', AccountSearchView.as_view(), name='account-search'),
    path('edit/<int:id>/', AccountUpdateView.as_view(), name='account-update'),
    path('<int:id>/', AccountDetailView.as_view(), name='account-detail'),
    path('del/<int:id>/', AccountDeleteView.as_view(), name='account-delete'),
]