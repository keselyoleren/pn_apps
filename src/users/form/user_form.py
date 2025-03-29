from django import forms
from django.contrib.auth.forms import UserCreationForm
from config.form import AbstractForm
from users.models import AccountUser

class AccountUserForm(UserCreationForm):
    class Meta:
        model = AccountUser
        fields = ['wilayah', 'role', 'username',  'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(AccountUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'username':
                self.fields['username'].widget.attrs['placeholder'] = 'Username'


class UserForm(AbstractForm):
    class Meta:
        model = AccountUser
        fields = ['wilayah', 'role',  'username', 'email', 'first_name', 'last_name']

    