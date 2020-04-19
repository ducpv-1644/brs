import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import authenticate

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
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
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

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(username=cleaned_data.get('email'),
                            password=cleaned_data.get('password'))
        msg = 'Email and password not matching!'
        if not user:
            raise ValidationError(msg)


class ChangeRoleAccountForm(forms.Form):
    username = forms.CharField(max_length=150)
    role = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'education', 'location', 'skills', 'notes']


class UserFollowForm(forms.Form):
    following_id = forms.IntegerField()
    status = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
