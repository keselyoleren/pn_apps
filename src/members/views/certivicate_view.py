# myapp/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.choice import RoleUser, Status, Tingkat
from config.permis import IsPublicAuth
from members.forms import CertificateForm, SuperUserCertificateForm
from members.models import Sertifikat
from django.db.models import Q


class CertificateListView(IsPublicAuth, ListView):
    model = Sertifikat
    template_name = 'members/list_certificate.html'
    context_object_name = 'sertifikat_list'
    paginate_by = 10  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.user.role == RoleUser.SANTRI:
            queryset = queryset.filter(user=self.request.user)
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(nomor_sertifikat__icontains=search_query) |
                Q(diterbitkan_oleh__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(tingkat__icontains=search_query)
            )
        
        # Sorting
        sort_field = self.request.GET.get('sort', 'tanggal_terbit')  # Default sort by date
        sort_direction = self.request.GET.get('direction', 'desc')  # Default newest first
        
        if sort_direction == 'desc':
            sort_field = f'-{sort_field}'
        
        return queryset.order_by(sort_field)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add search and sorting context
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'current_sort': self.request.GET.get('sort', 'tanggal_terbit'),
            'current_direction': self.request.GET.get('direction', 'desc'),
            'tingkat_choices': Tingkat.choices,
            'btn_add': True,
            'create_url': reverse_lazy('certificate-create'),
            'header_title': 'List Sertifikat',
            'header': 'List Sertifikat'
        })

        
        return context

class CertificateCreateView(IsPublicAuth, CreateView):
    model = Sertifikat
    template_name = 'component/form.html'
    success_url = reverse_lazy('certificate-list')

    def get_form_class(self):
        user = self.request.user
        
        if user.role == RoleUser.SANTRI:
            return CertificateForm
        else: 
            return SuperUserCertificateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Sertifikat'
        context['header_title'] = 'Tambah Sertifikat'
        return context

    def form_valid(self, form):
        if self.request.user.role == RoleUser.SANTRI:
            form.instance.user = self.request.user
        return super().form_valid(form)

class CertificateUpdateView(IsPublicAuth, UpdateView):
    model = Sertifikat
    template_name = 'component/form.html'
    success_url = reverse_lazy('certificate-list')

    def get_form_class(self):
        user = self.request.user
        
        if user.role == RoleUser.SANTRI:
            return CertificateForm
        else: 
            return SuperUserCertificateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Sertifikat'
        context['header_title'] = 'Edit Sertifikat'
        return context
    
    def form_valid(self, form):
        if self.request.user.role == RoleUser.SANTRI:
            form.instance.user = self.request.user
        return super().form_valid(form)

class CertificateDetailView(IsPublicAuth, DetailView):
    model = Sertifikat
    template_name = 'certificate/detail.html'
    context_object_name = 'sertifikat'  # Gunakan ini agar lebih eksplisit
    success_url = reverse_lazy('certificate-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Serifikat'
        context['header_title'] = 'Serifikat Detail'
        return context

class CertificateDeleteView(IsPublicAuth, DeleteView):
    model = Sertifikat
    template_name = 'component/delete.html'
    success_url = reverse_lazy('certificate-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Sertifikat'
        context['header_title'] = 'Delete Sertifikat'
        return context
