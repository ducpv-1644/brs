from django.urls import path

from .views import (
    UserDetailView,
    AdminDashboardView,
    UserUpdateView,
    SignUpView,
    SignInView,
    SignOutView,
    UserListView,
    ChangeRoleUserView,
    UserFollowUpdateCreateView,
    UserFollowedListView
)

app_name = 'users'

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('signin', SignInView.as_view(), name='signin'),
    path('signout', SignOutView.as_view(), name='signout'),

    path('user/<int:id>/change-role/', ChangeRoleUserView.as_view(), name='change-role'),
    path('users/', UserListView.as_view(), name='users-list'),
    path('user/<int:id>/edit/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    path('user/follow/', UserFollowUpdateCreateView.as_view(), name='user-follow'),
    path('user/followed/', UserFollowedListView.as_view(), name='user-followed')
]