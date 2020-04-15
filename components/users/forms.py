import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User
from utility.utility import verify_email_format


class SignUpForm(UserCreationForm):
    terms = forms.CharField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'terms']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is exist!')
        if not verify_email_format(self.cleaned_data.get('email')):
            raise ValidationError("Email is not Sun Asterisk email")

        return email

    def clean_terms(self):
        if self.cleaned_data['terms'] != 'on':
            raise ValidationError("You forgot check on terms")

        return True

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError("Password and confirm password not match")

    def save(self, commit=True):
        data = self.cleaned_data
        user = User.objects.create(
            email=data.get('email'),
            username=data.get('email'),
            is_activate=True
        )
        user.set_password(data.get('password1'))
        user.last_login = datetime.datetime.now()
        user.save()

        return user


class SignInForm(forms.Form):
    email = forms.CharField(min_length=1, max_length=150)
    password = forms.CharField(min_length=1, max_length=128)


class ChangeRoleAccountForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=150, label='Username')
    role = forms.ChoiceField(choices=User.USER_ROLES)


class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['avatar']
