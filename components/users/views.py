from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from .forms import (
    SignInForm, SignUpForm,
    ChangeRoleAccountForm,
    AccountUpdateForm
)
from .models import User
from .decorators import admin_required


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
            return redirect(reverse('book:book-list'))
        return render(request, self.template_name, {'form': self.form_class})


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users:signin'))


class ChangeRoleAccountView(View):
    template_name = 'change_user_role.html'
    form_class = ChangeRoleAccountForm

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        change_role_account_form = ChangeRoleAccountForm(request.POST)
        if change_role_account_form.is_valid():
            user = User.objects.filter(username=change_role_account_form.cleaned_data['username']).first()
            if user:
                user.role = int(change_role_account_form.cleaned_data['role'])
                user.save()
                return redirect(reverse('users:users-list'))
            return render(request, '404.html', {'message': f'User {user.username} not found'})


class AccountListView(View):
    template_name = 'users_list.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_activate=True)
        return render(request, self.template_name, {'users': users})


class AccountUpdateView(View):
    form_class = AccountUpdateForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user_update_form = AccountUpdateForm(request.POST)
        if user_update_form.is_valid():
            user = User.objects.filter(id=kwargs.get('id')).first()
            if not user:
                return render(request, '404.html', {'message': 'User not found'})
            user.username = user_update_form.cleaned_data['username']
            user.email = user_update_form.cleaned_data['username']
            user.education = user_update_form.cleaned_data['education']
            user.skills = user_update_form.cleaned_data['skills']
            user.notes = user_update_form.cleaned_data['notes']
            user.location = user_update_form.cleaned_data['location']
            user.save()

            return redirect(reverse('users:user-detail', kwargs={'id': user.id}))


class AccountDetailView(View):
    template_name = 'user_detail.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=kwargs.get('id')).first()
        if not user:
            return render(request, '404.html', {'message': 'User not found'})
        return render(request, self.template_name, {'member': user})


class AccountDeleteView(View):

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        account = get_object_or_404(kwargs.get('id'))
        account.user.is_active = False
        account.user.save()

        return redirect(reverse('users:account-list'))


class AccountSearchView(View):
    template_name = 'account_list.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        search_text = request.GET.get('q')
        accounts_qs = Account.objects.annotate(
            search=SearchVector(
                'user__username', 'user__email'
            )
        ).filter(search=search_text).distinct('user__username')

        return render(request, self.template_name, {'accounts': accounts_qs})
