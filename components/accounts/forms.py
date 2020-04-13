from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Account


class SignUpForm(UserCreationForm):
    terms = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'terms']


class SignInForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=150, label='Username')
    password = forms.CharField(min_length=1, max_length=128, label='Password')


class ChangeRoleAccountForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=150, label='Username')
    role = forms.ChoiceField(choices=Account.ROLE_CHOICES)


class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['avatar']
