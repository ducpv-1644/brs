from django import forms

from .models import Account


class SignInForm(forms.Form):
    username = forms.CharField(min_length=1 ,max_length=150, label='Username')
    password = forms.CharField(min_length=1, max_length=128, label='Password')


class ChangeRoleAccountForm(forms.Form):
    username = forms.CharField(min_length=1 ,max_length=150, label='Username')
    role = forms.ChoiceField(choices=Account.ROLE_CHOICES)


class AccountUpdateForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['avatar']