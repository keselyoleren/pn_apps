# myapp/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from config.permis import IsAuthenticated
from django.db.models import Q

from members.forms import PerguruanForm
from members.models import Perguruan

class PerguruanListView(IsAuthenticated, ListView):
    model = Perguruan
    template_name = 'perguruan/list.html'
    context_object_name = 'list_perguruan'
    paginate_by = 10  # Number of items per page
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) 
            )
        
        # Sorting
        sort_field = self.request.GET.get('sort', 'nama')  # Default sort by Perguruanname
        sort_direction = self.request.GET.get('nama', 'asc')
        
        if sort_direction == 'desc':
            sort_field = f'-{sort_field}'
        
        return queryset.order_by(sort_field)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Perguruan'
        context['header_title'] = 'List Perguruan'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('perguruan-create')
        
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'current_sort': self.request.GET.get('sort', 'nama'),
            'current_direction': self.request.GET.get('nama', 'asc'),
        })
        
        return context

class PerguruanCreateView(IsAuthenticated, CreateView):
    model = Perguruan
    template_name = 'component/form.html'
    form_class = PerguruanForm
    success_url = reverse_lazy('perguruan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Perguruan'
        context['header_title'] = 'Tambah Perguruan'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class PerguruanUpdateView(IsAuthenticated, UpdateView):
    model = Perguruan
    template_name = 'component/form.html'
    form_class = PerguruanForm
    success_url = reverse_lazy('perguruan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Perguruan'
        context['header_title'] = 'Edit Perguruan'
        return context

class PerguruanDeleteView(IsAuthenticated, DeleteView):
    model = Perguruan
    template_name = 'component/delete.html'
    success_url = reverse_lazy('perguruan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Perguruan'
        context['header_title'] = 'Delete Perguruan'
        return context
