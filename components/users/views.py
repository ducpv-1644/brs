from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View

from .forms import (
    SignInForm, SignUpForm,
    ChangeRoleAccountForm,
    UserUpdateForm, UserFollowForm
)

from components.books.models import Book, BookRequestBuy

from .models import User, UserFollow
from .decorators import admin_required
from utility.log_activity import ActivityLog

logger = ActivityLog()


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': UserCreationForm})

    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)

            return redirect(reverse('book:book-list'))
        return render(request, self.template_name, {'form': signup_form})


class SignInView(View):
    template_name = 'signin.html'
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        signin_form = self.form_class(request.POST)
        if signin_form.is_valid():
            user = authenticate(username=signin_form.cleaned_data['email'],
                                password=signin_form.cleaned_data['password'])
            login(request, user)
            if user and user.role == 2:
                return redirect(reverse('book:book-list'))
            elif user and user.role == 1:
                return redirect(reverse('users:dashboard'))
        return render(request, self.template_name, {'form': signin_form})


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users:signin'))


class UserListView(View):
    template_name = 'users_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_activate=True)
        return render(request, self.template_name, {'users': users})


class UserDetailView(View):
    template_name = 'user_detail.html'
    LIMIT_ACTIVITY = 10

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=kwargs.get('id')).first()
        activity_log = logger.get_activity_log(user=user, limit=10)
        if not user:
            return render(request, '404.html', {'message': 'User not found'})

        follow_qs = UserFollow.objects.filter(follower=request.user, following=user).first()
        follow_status = 1 if not follow_qs else follow_qs.status
        following_count = UserFollow.objects.filter(follower=user, status=UserFollow.STATUS_FOLLOW[1][0]).count()
        follower_count = UserFollow.objects.filter(following=user, status=UserFollow.STATUS_FOLLOW[1][0]).count()
        context = {
            'member': user,
            'activities': activity_log,
            'follow_status': follow_status,
            'following_count': following_count,
            'follower_count': follower_count,
            'form_role': kwargs.get('form_role'),
            'form_profile': kwargs.get('form_profile'),
            'form_follow': kwargs.get('form_follow')
        }
        return render(request, self.template_name, context=context)


class UserUpdateView(UserDetailView):
    form_class = UserUpdateForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user_update_form = UserUpdateForm(request.POST)
        if user_update_form.is_valid():
            if request.user.id != kwargs.get('id') and request.user.role != 1:
                return HttpResponseForbidden('403 Forbidden')

            user = User.objects.filter(id=kwargs.get('id')).first()
            if not user:
                return render(request, '404.html', {'message': 'User not found'})
            user.username = user_update_form.cleaned_data['username']
            user.email = user_update_form.cleaned_data['username']
            user.education = user_update_form.cleaned_data['education']
            user.skills = user_update_form.cleaned_data['skills']
            user.notes = user_update_form.cleaned_data['notes']
            user.location = user_update_form.cleaned_data['location']
            if request.FILES.get('avatar'):
                user.avatar = request.FILES['avatar']
            user.save()

            return redirect(reverse('users:user-detail', kwargs={'id': user.id}))
        kwargs.update({'form_profile': user_update_form})
        response = self.get(request, *kwargs)
        return response


class ChangeRoleUserView(UserDetailView):
    form_class = ChangeRoleAccountForm

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        change_role_account_form = ChangeRoleAccountForm(request.POST)
        if change_role_account_form.is_valid():
            username = change_role_account_form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if user:
                user.role = int(change_role_account_form.cleaned_data['role'])
                user.save()
                return redirect(reverse('users:user-detail', kwargs={'id': user.id}))
            return render(request, '404.html', {'message': f'User {user.username} not found'})

        kwargs.update({'form_role': change_role_account_form})
        response = self.get(request, **kwargs)
        return response


class UserFollowUpdateCreateView(UserDetailView):
    form_class = UserFollowForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        follow_form = self.form_class(request.POST)
        if follow_form.is_valid():
            follower = request.user
            following = follow_form.cleaned_data['following_id']
            status = follow_form.cleaned_data['status']
            follow_qs = UserFollow.objects.filter(follower=follower, following__id=following).first()
            if not follow_qs:
                UserFollow.objects.create(follower=follower, following__=following, status=status)
            else:
                follow_qs.status = status
                follow_qs.save()

            return redirect(reverse('users:user-detail', kwargs={'id': following}))
        kwargs.update({'form_follow': follow_form})
        response = self.get(request, **kwargs)
        return response


class AdminDashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        users_count = User.objects.all().count()
        books_count = Book.objects.all().count()
        books_request_buy_count = BookRequestBuy.objects.filter(status=BookRequestBuy.STATUS_CHOICES[0][0]).count()
        context = {
            'users_count': users_count,
            'books_count': books_count,
            'books_request_buy_count': books_request_buy_count

        }
        return render(request, self.template_name, context=context)
