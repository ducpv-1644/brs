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
from .models import Account
from .decorators import admin_required


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': UserCreationForm})

    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid() and signup_form.cleaned_data['terms'] == 'on':
            signup_form.save()
            user = authenticate(username=signup_form.cleaned_data['username'],
                                password=signup_form.cleaned_data['password1'])
            Account.objects.get_or_create(user=user)
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
            user = authenticate(username=signin_form.cleaned_data['username'],
                                password=signin_form.cleaned_data['password'])
            login(request, user)
            return redirect(reverse('book:book-list'))
        return render(request, self.template_name, {'form': self.form_class})


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('account:signin'))


class ChangeRoleAccountView(View):
    template_name = 'change_role_account.html'
    form_class = ChangeRoleAccountForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        change_role_account_form = ChangeRoleAccountForm(request.POST)
        if change_role_account_form.is_valid():
            Account.objects.filter(
                user__username=change_role_account_form.cleaned_data['username']
            ).update(
                role=change_role_account_form.cleaned_data['role']
            )
        return redirect(reverse('account:account-list'))


class AccountListView(View):
    template_name = 'account_list.html'

    def get(self, request, *args, **kwargs):
        accounts_qs = Account.objects.filter(user__is_active=True)
        return render(request, self.template_name, {'accounts': accounts_qs})


class AccountUpdateView(View):
    template_name = 'account_update.html'
    form_class = AccountUpdateForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        account = self.__get_user_id(request, **kwargs)
        if not account:
            return HttpResponseForbidden('403 Forbidden')

        init_data = {
            'email': account.user.email,
            'avatar': account.avatar
        }
        account_update_form = self.form_class(initial=init_data)
        return render(request, self.template_name, {'form': account_update_form, 'id': account.id})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        account_update_form = AccountUpdateForm(request.POST)
        if account_update_form.is_valid():
            email = account_update_form.cleaned_data['email']
            avatar = account_update_form.cleaned_data['avatar']

            account = self.__get_user_id(request, **kwargs)
            account.user.email = email
            account.user.save()

            account.avatar = avatar
            account.save()

            return redirect(reverse('account:account-detail', kwargs={'id': account.id}))

    def __get_user_id(self, request, **kwargs):
        account = get_object_or_404(Account, pk=kwargs.get('id'))
        if (account.role == '1' and request.user.id == account.user.id) or account.role == '0':
            return account


class AccountDetailView(View):
    template_name = 'account_detail.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('id')
        account = get_object_or_404(Account, pk=account_id)
        if account.user.id != request.user.id:
            return HttpResponseForbidden('403 Forbidden')
        return render(request, self.template_name, {'account': account})


class AccountDeleteView(View):

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        account = get_object_or_404(kwargs.get('id'))
        account.user.is_active = False
        account.user.save()

        return redirect(reverse('account:account-list'))


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
