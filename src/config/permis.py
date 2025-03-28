from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render

from config.choice import RoleUser



class AccessMixin:
    """
    Abstract CBV mixin that gives access mixins the same customizable
    functionality.
    """
    login_url = "/auth/login/"
    login_user_url = '/auth/login/'
    permission_denied_message = 'Hayoo mau ngapain.. awas lo.. kena uu ITE..!!'
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        """
        Override this method to override the login_url attribute.
        """
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    def get_permission_denied_message(self):
        """
        Override this method to override the permission_denied_message attribute.
        """
        return self.permission_denied_message

    def get_redirect_field_name(self):
        """
        Override this method to override the redirect_field_name attribute.
        """
        return self.redirect_field_name

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def handle_no_user_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.login_user_url, self.get_redirect_field_name())
    
    


class LoginUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) if request.user.is_authenticated else self.handle_no_user_permission()


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) if request.user.is_authenticated else self.handle_no_permission()



class IsLoginAuthenticated(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

class LoginViewMixinUser(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
        
class IsAuthenticated(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs) 
        else:
            return self.handle_no_permission()


class IsPublicAuth(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs) 
        else:
            self.handle_no_permission()


class IsUser(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role == RoleUser.USER or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()