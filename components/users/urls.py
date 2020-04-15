from django.urls import path

from .views import (
    AccountDetailView,
    AdminDashboardView,
    AccountUpdateView,
    SignUpView,
    SignInView,
    SignOutView,
    AccountListView,
    ChangeRoleAccountView
)

app_name = 'users'

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('signin', SignInView.as_view(), name='signin'),
    path('signout', SignOutView.as_view(), name='signout'),

    path('user/change-role', ChangeRoleAccountView.as_view(), name='change-role'),
    path('users/', AccountListView.as_view(), name='users-list'),
    path('user/<int:id>/edit/', AccountUpdateView.as_view(), name='user-update'),
    path('user/<int:id>/', AccountDetailView.as_view(), name='user-detail'),
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
]