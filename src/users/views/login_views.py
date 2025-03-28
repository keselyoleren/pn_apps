
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib import messages
from users.form.login_form import AdminPasswordChangeForm, LoginForm, ProfileForm
from django.views.generic import  UpdateView

from config.permis import IsAuthenticated, IsLoginAuthenticated, LoginRequiredMixin

from django.views.generic.edit import UpdateView
from config.choice import RoleUser
from django.contrib.auth.views import PasswordChangeView


from users.models import AccountUser

class UserLoginView(IsLoginAuthenticated ,LoginView):
    template_name = 'auth/login.html'
    form_class = LoginForm

    def get_success_url(self) -> str:
        return "/"

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LogoutCustomerView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutCustomerView, self).get(request, *args, **kwargs)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'component/form.html'
    form_class = AdminPasswordChangeForm

    def get_success_url(self) -> str:
        return '/'

    def get_template_names(self):
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Ganti Password'
        context['header_title'] = 'Ganti Password'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Ganti Password Success..")
        return super().form_valid(form)

class ChangePasswordAdminView(IsAuthenticated, PasswordChangeView):
    template_name = 'component/form.html'
    form_class = AdminPasswordChangeForm

    def get_success_url(self):
        return '/admin-panel/dashboard'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.kwargs['user_id']
        user = AccountUser.objects.get(id=user_id)
        kwargs['user'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = AccountUser.objects.get(id=user_id)
        context['header'] = f'Ganti Password {user}'
        context['header_title'] = f'Ganti Password {user}'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Sandi berhasil diubah.')
        return super().form_valid(form)


class ProfileUserApiView(LoginRequiredMixin, UpdateView):
    model = AccountUser
    template_name = 'component/form.html'
    form_class = ProfileForm
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['header'] = 'Profile'
        context['header_title'] = 'Update Profile'
        context['is_profile'] = True
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def get_template_names(self):
        return super().get_template_names()

    def get_success_url(self):
        # Redirect to the profile page after successful form submission
        messages.success(self.request, "Profile berhasil di update")
        return '/'
        
