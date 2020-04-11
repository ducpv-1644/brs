from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.views import View


class SignUpView(View):
    template_name = 'sign_up.html'
    success_url = '/book/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': UserCreationForm})

    def post(self, request, *args, **kwargs):
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            user = authenticate(username=sign_up_form.username, password=sign_up_form.password1)
            login(request, user)

            return redirect(self.success_url)


class SignInView(View):
    template_name = 'sign_in.html'
    success_url = '/book/'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class SignOutView(View):
    success_url = '/book/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)


class CreateAccountView(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class UpdateAccountView(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class DetailAccountView(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class DeleteAccountView(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
