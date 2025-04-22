# myapp/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.choice import RoleUser, Status
from config.permis import IsPublicAuth
from members.forms import IKTForm, SuperUserIKTForm
from members.models import IKT, Members
from django.db.models import Q

from users.models import AccountUser


class IKTListView(IsPublicAuth, ListView):
    model = IKT
    template_name = 'ikt/list.html'
    context_object_name = 'ikt_users'
    paginate_by = 10  # Number of items per page
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):  # Fixed typo in method name (was get_quweyset)
        user = self.request.user
        queryset = super().get_queryset()
        
        # Role-based filtering
        if user.role == RoleUser.SANTRI:
            queryset = queryset.filter(user=user)
        elif user.role == RoleUser.PAC:
            member = Members.objects.filter(kecamatan=user.wilayah).values_list('user', flat=True)
            queryset = queryset.filter(user__in=member)
        elif user.role == RoleUser.PC:
            member = Members.objects.filter(kabupaten=user.kabupaten).values_list('user', flat=True)
            queryset = queryset.filter(user__in=member)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(nomor_sertifikat=search_query)
            )
        
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Ordering
        order_by = self.request.GET.get('order_by')
        if order_by in ['user__usernmae', 'nomor_sertifikat', 'naik_ke_tingkat', 'status', 'created_at']:
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('order') == 'desc':
                queryset = queryset.order_by(f'-{order_by}')
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'IKT (Imtihan Kenaikan Tingkat)'
        context['header_title'] = 'List IKT (Imtihan Kenaikan Tingkat)'
        if self.request.user.role == RoleUser.PAC:
            context['btn_add'] = False
        else:
            context['btn_add'] = True
            context['create_url'] = reverse_lazy('ikt-create') 
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        # Add ordering information to context
        order_by = self.request.GET.get('order_by', 'created_at')
        context['order_by'] = order_by
        context['order'] = self.request.GET.get('order', 'desc')
        
        return context

class IKTCreateView(IsPublicAuth, CreateView):
    model = IKT
    template_name = 'component/form.html'
    success_url = reverse_lazy('ikt-list')

    def get_form_class(self):
        user = self.request.user
        
        if user.role == RoleUser.SANTRI:
            return IKTForm
        else: 
            return SuperUserIKTForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'IKT (Imtihan Kenaikan Tingkat)'
        context['header_title'] = 'Ajukan IKT (Imtihan Kenaikan Tingkat)'
        return context

    def form_valid(self, form):
        if self.request.user.role == RoleUser.SANTRI:
            form.instance.user = self.request.user
        return super().form_valid(form)

class IKTUpdateView(IsPublicAuth, UpdateView):
    model = IKT
    template_name = 'component/form.html'
    success_url = reverse_lazy('ikt-list')

    def get_form_class(self):
        user = self.request.user
        
        if user.role == RoleUser.SANTRI:
            return IKTForm
        else: 
            return SuperUserIKTForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'IKT (Imtihan Kenaikan Tingkat)'
        context['header_title'] = 'Edit IKT (Imtihan Kenaikan Tingkat)'
        return context
    
    def form_valid(self, form):
        if self.request.user.role == RoleUser.SANTRI:
            form.instance.user = self.request.user
        print(form.instance.user)
        return super().form_valid(form)

class IKTDetailView(IsPublicAuth, DetailView):
    model = IKT
    template_name = 'ikt/detail.html'
    context_object_name = 'ikt'  # Gunakan ini agar lebih eksplisit
    success_url = reverse_lazy('ikt-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'IKT (Imtihan Kenaikan Tingkat)'
        context['header_title'] = 'Detail IKT (Imtihan Kenaikan Tingkat)'
        return context

class IKTDeleteView(IsPublicAuth, DeleteView):
    model = IKT
    template_name = 'component/delete.html'
    success_url = reverse_lazy('ikt-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'IKT (Imtihan Kenaikan Tingkat)'
        context['header_title'] = 'Delete IKT (Imtihan Kenaikan Tingkat)'
        return context
