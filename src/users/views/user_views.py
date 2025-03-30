# myapp/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from config.permis import IsAuthenticated
from users.form.user_form import AccountUserForm, UserForm
from users.models import AccountUser
from django.db.models import Q

class AccountUserListView(IsAuthenticated, ListView):
    model = AccountUser
    template_name = 'users/list.html'
    context_object_name = 'list_users'
    paginate_by = 10  # Number of items per page
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(role__icontains=search_query)
            )
        
        # Sorting
        sort_field = self.request.GET.get('sort', 'username')  # Default sort by username
        sort_direction = self.request.GET.get('direction', 'asc')
        
        if sort_direction == 'desc':
            sort_field = f'-{sort_field}'
        
        return queryset.order_by(sort_field)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'List User'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('user-create')
        
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'current_sort': self.request.GET.get('sort', 'username'),
            'current_direction': self.request.GET.get('direction', 'asc'),
        })
        
        return context

class AccountUserCreateView(IsAuthenticated, CreateView):
    model = AccountUser
    template_name = 'users/form.html'
    form_class = AccountUserForm
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'Tambah User'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class AccountUserUpdateView(IsAuthenticated, UpdateView):
    model = AccountUser
    template_name = 'users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'Edit User'
        return context

class AccountUserDeleteView(IsAuthenticated, DeleteView):
    model = AccountUser
    template_name = 'component/delete.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'Delete User'
        return context
