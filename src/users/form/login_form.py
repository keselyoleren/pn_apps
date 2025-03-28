

from django.core.exceptions import ValidationError

from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from config.form import AbstractForm
from users.models import AccountUser

UserModel = get_user_model()


class EmailAuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "email" field.
        username_max_length = UserModel._meta.get_field(UserModel.USERNAME_FIELD).max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(UserModel._meta.get_field(UserModel.USERNAME_FIELD).verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise self.get_invalid_login_error()
        else:
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': UserModel._meta.get_field(UserModel.USERNAME_FIELD).verbose_name},
        )


class LoginForm(EmailAuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control', 'pnameholder': 'Password'}),
    )

    
    
class ProfileForm(AbstractForm):
    class Meta:
        model = AccountUser
        fields = ['username', 'email', 'first_name', 'last_name']

class AdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    required_css_class = 'required'
    password1 = forms.CharField(
        label=_("Password Baru"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 
            'autofocus': True,
            'class':'form-control'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Konfirmasi Password"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class':'form-control'
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    @property
    def changed_data(self):
        data = super().changed_data
        for name in self.fields:
            if name not in data:
                return []
        return ['password']
