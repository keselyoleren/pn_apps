from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.views.generic import TemplateView
from config.choice import RoleUser
from config.permis import IsPublicAuth, IsLoginAuthenticated, LoginRequiredMixin
from members.forms import MembersForm, SuperUserMembersForm
from members.models import Members
from users.models import AccountUser
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from django.db.models import Count, Q
from django.http import JsonResponse

def anggota_stats(request):
    # Data untuk card summary
    total_anggota = Members.objects.count()
    anggota_laki = Members.objects.filter(jenis_kelamin='L').count()
    anggota_perempuan = Members.objects.filter(jenis_kelamin='P').count()
    
    # Data untuk grafik
    kecamatan_data = Members.objects.exclude(kecamatan__isnull=True)\
                                  .exclude(kecamatan__exact='')\
                                  .values('kecamatan')\
                                  .annotate(total=Count('id'))\
                                  .order_by('-total')[:10]  # Ambil 10 teratas
    
    labels = [item['kecamatan'] for item in kecamatan_data]
    values = [item['total'] for item in kecamatan_data]
    
    # Data untuk pie chart jenis kelamin
    gender_data = {
        'labels': ['Laki-laki', 'Perempuan'],
        'data': [anggota_laki, anggota_perempuan]
    }
    
    return JsonResponse({
        'total_anggota': total_anggota,
        'gender_data': gender_data,
        'kecamatan_data': {
            'labels': labels,
            'data': values
        }
    })

class IndexPage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Dashboard'
        context['header_title'] = 'Dashboard'
        return context

class MembersCreateView(CreateView):
    model = Members
    template_name = 'members/register.html'
    form_class = MembersForm
    success_url = reverse_lazy('login')  

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Member'
        context['header_title'] = 'Register Member'
        return context

    def form_valid(self, form):
        response =  super().form_valid(form)
        email = form.cleaned_data.get('email')
        nik = form.cleaned_data.get('nik')
        user, created = AccountUser.objects.get_or_create(
            username=nik, 
            email=email,
            first_name=form.cleaned_data.get('nama'),
            role=RoleUser.MEMBER,
            kabupaten=form.cleaned_data.get('kabupaten'),
            wilayah=form.cleaned_data.get('kecamatan'),
            defaults={'email': email}
        )
        # set password
        user.set_password("default")
        user.save()
        self.object.user = user
        self.object.save()
        messages.success(self.request, "Registrasi berhasil, silahkan login dengan username dengan 'NIK' anda dan password 'default'")
        return response

class MemebersAdminCreateView(IsPublicAuth, CreateView):
    model = Members
    template_name = 'component/form.html'
    form_class = MembersForm
    success_url = reverse_lazy('member-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Anngota'
        context['header_title'] = 'Add Anggota'
        return context

    def form_valid(self, form):
        return  super().form_valid(form)
        

class MembersListView(IsPublicAuth, ListView):
    model = Members
    template_name = 'members/list.html'
    context_object_name = 'list_members'
    paginate_by = 10  # Number of items per page
    
    def get_queryset(self):
        user_wilayah = self.request.user.wilayah
        queryset = super().get_queryset()
        
        # Apply role-based filtering
        if self.request.user.is_superuser:
            queryset = Members.objects.all()
        elif self.request.user.role == RoleUser.MEMBER:
            queryset = Members.objects.filter(user=self.request.user)
        elif self.request.user.role == RoleUser.PC:
            queryset = Members.objects.filter(kabupaten=self.request.user.kabupaten)
        elif self.request.user.role == RoleUser.PAC:
            queryset = Members.objects.filter(kecamatan=user_wilayah)
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(nik__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(nama__icontains=search_query) |
                Q(kecamatan__icontains=search_query) |
                Q(kabupaten__icontains=search_query) |
                Q(provinsi__icontains=search_query) |
                Q(no_hp__icontains=search_query) |
                Q(unit_latihan__icontains=search_query) |
                Q(jenis_kelamin__icontains=search_query) |
                Q(tempat_lahir__icontains=search_query) |
                Q(tgl_lahir__icontains=search_query) |
                Q(kelurahan__icontains=search_query)
            )
        
        # Sorting
        sort_field = self.request.GET.get('sort', 'nama')  # Default sort by name
        sort_direction = self.request.GET.get('direction', 'asc')
        
        if sort_direction == 'desc':
            sort_field = f'-{sort_field}'
        
        return queryset.order_by(sort_field)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.role == RoleUser.MEMBER:
            context.update({
                'header': 'Data diri',
                'header_title': 'Data diri',
                'btn_add': False
            })
        else:
            header_title = 'List Anggota'
            if not user.is_superuser and user.role == RoleUser.ADMIN:
                header_title = f'List Anggota wilayah {user.wilayah}'
                
            context.update({
                'header': 'Anggota',
                'header_title': header_title,
                'btn_add': True,
                'create_url': reverse_lazy('member-create'),
                'search_query': self.request.GET.get('search', ''),
                'current_sort': self.request.GET.get('sort', 'nama'),
                'current_direction': self.request.GET.get('direction', 'asc'),
            })
        
        return context


class MembersUpdateView(IsPublicAuth, UpdateView):
    model = Members
    template_name = 'component/form.html'
    success_url = reverse_lazy('member-list')

    def get_form_class(self):
        user = self.request.user        
        if user.role == RoleUser.MEMBER:
            return MembersForm
        else: 
            return SuperUserMembersForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == RoleUser.MEMBER:
            context['header'] = 'Data diri'
            context['header_title'] = 'Edit data diri'
        else:
            context['header'] = 'Anggota'
            context['header_title'] = 'Edit Anggota'
        return context
    
    def form_valid(self, form):
        if self.request.user.role == RoleUser.MEMBER:
            form.instance.user = self.request.user
        return super().form_valid(form)

class MembersDeleteView(IsPublicAuth, DeleteView):
    model = Members
    template_name = 'component/delete.html'
    success_url = reverse_lazy('member-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Anggota'
        context['header_title'] = 'Delete Anggota'
        return context

def get_wilayah(request):
    kecamatan = request.GET.get('kecamatan')
    wilayah = Members.objects.filter(kecamatan=kecamatan).order_by('kelurahan').values('kelurahan').distinct()
    return render(request, 'component/wilayah.html', {'wilayah': wilayah})

class MemberDetailView(IsPublicAuth, DetailView):
    model = Members
    template_name = 'members/detail.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Anggota'
        context['header_title'] = 'Detail Anggota'
        return context