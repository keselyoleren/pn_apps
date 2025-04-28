from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from config.choice import RoleUser
from config.permis import IsPublicAuth, IsLoginAuthenticated, LoginRequiredMixin
from members.forms import BulkUploadForm, MembersForm, SuperUserMembersForm
from members.models import Members, Perguruan
from users.models import AccountUser
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.template.loader import get_template
from django.http import HttpResponse

import pandas as pd
from io import BytesIO

from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse

from xhtml2pdf import pisa


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
            role=RoleUser.SANTRI,
            kabupaten=form.cleaned_data.get('kabupaten'),
            wilayah=form.cleaned_data.get('kecamatan'),
            defaults={'email': email}
        )
        # set password
        user.set_password("pagarnusabwi1985.1986")
        user.save()
        self.object.user = user
        self.object.save()
        nama_pelatih = Members.objects.filter(nama=self.object.nama_pelatih).first()
        if nama_pelatih:
            self.object.parent = nama_pelatih
        self.object.save()
        messages.success(self.request, "Registrasi berhasil, silahkan login dengan username dengan 'NIK' anda dan password 'pagarnusabwi1985.1986'")
        return response

class MemebersAdminCreateView(IsPublicAuth, CreateView):
    model = Members
    template_name = 'members/form.html'
    form_class = MembersForm
    success_url = reverse_lazy('member-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Anggota'
        context['header_title'] = 'Add Anggota'
        return context

    def form_valid(self, form):
        response =  super().form_valid(form)
        email = form.cleaned_data.get('email')
        nik = form.cleaned_data.get('nik')
        user, created = AccountUser.objects.get_or_create(
            username=nik, 
            email=email,
            first_name=form.cleaned_data.get('nama'),
            role=RoleUser.SANTRI,
            kabupaten=form.cleaned_data.get('kabupaten'),
            wilayah=form.cleaned_data.get('kecamatan'),
            defaults={'email': email}
        )
        # set password
        user.set_password("pagarnusabwi1985.1986")
        user.save()
        self.object.user = user
        self.object.save()
        nama_pelatih = Members.objects.filter(nama=self.object.nama_pelatih).first()
        if nama_pelatih:
            self.object.parent = nama_pelatih
        self.object.save()
        messages.success(self.request, "Registrasi berhasil, silahkan login dengan username dengan 'NIK' anda dan password 'pagarnusabwi1985.1986'")
        return response
        

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
        elif self.request.user.role == RoleUser.SANTRI:
            queryset = Members.objects.filter(user=self.request.user)
        elif self.request.user.role == RoleUser.PC:
            queryset = Members.objects.filter(kabupaten=self.request.user.kabupaten)
        elif self.request.user.role == RoleUser.PELATIH_CABANG:
            pelatih_cabang = Members.objects.filter(user=self.request.user).first()
            queryset = Members.objects.filter(Q(parent=pelatih_cabang)| Q(user=self.request.user))
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
        
        if user.role == RoleUser.SANTRI:
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
    template_name = 'members/form.html'
    success_url = reverse_lazy('member-list')

    def get_form_class(self):
        user = self.request.user        
        if user.role == RoleUser.SANTRI:
            return MembersForm
        else: 
            return SuperUserMembersForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == RoleUser.SANTRI:
            context['header'] = 'Data diri'
            context['header_title'] = 'Edit data diri'
        else:
            context['header'] = 'Anggota'
            context['header_title'] = 'Edit Anggota'
        return context
    
    def form_valid(self, form):
        if self.request.user.role == RoleUser.SANTRI:
            form.instance.user = self.request.user
        pelatih_cabang = Members.objects.filter(nama=form.instance.nama_pelatih).first()
        form.instance.parent = pelatih_cabang
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
    
class MemberPDFView(IsPublicAuth, DetailView):
    model = Members
    template_name = 'members/biodata_pdf.html'  # ini template khusus pdf
    context_object_name = 'member'

    def get(self, request, *args, **kwargs):
        member = self.get_object()
        template_path = self.template_name
        context = {
            'member': member,
            'header': 'Anggota',
            'header_title': 'Detail Anggota (PDF)',
            'host':f"{self.request.scheme}://{self.request.get_host()}"
        }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="member_{member.nama}.pdf"'

        # Render HTML ke string
        template = get_template(template_path)
        html = template.render(context)

        # Create PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Terjadi error saat membuat PDF', status=500)
        return response
    
def pelatih_cabang_list(request):
    search = request.GET.get('search', '')
    queryset = Members.objects.filter(
        user__role=RoleUser.PELATIH_CABANG, 
        nama__icontains=search
    )

    results = []
    for member in queryset[:10]:  # limit hasil supaya ringan
        results.append({
            'nama': member.nama,
        })

    return JsonResponse(results, safe=False)

class MembersBulkUploadView(IsPublicAuth, FormView):
    template_name = 'members/bulk_upload.html'
    form_class = BulkUploadForm  # You'll need to create this form
    success_url = reverse_lazy('member-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Anggota'
        context['header_title'] = 'Bulk Upload Anggota'
        return context

    def form_valid(self, form):
        excel_file = form.cleaned_data['excel_file']
        
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)
            
            # Process each row
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    perguruan_value = row.get('perguruan')
                    perguruan = None
                    pelatih_cabang = Members.objects.filter(nama=row.get('nama_pelatih')).first()
                    parent = None
                    if pelatih_cabang:
                        parent = pelatih_cabang
                    if perguruan_value:
                        perguruan, _ = Perguruan.objects.get_or_create(
                            nama=perguruan_value,
                            defaults={'nama': perguruan_value}
                        )
                    # Create or update Member
                    member, created = Members.objects.update_or_create(
                        nik=row['nik'],
                        defaults={
                            'email': row['email'],
                            'nama': row['nama'],
                            'tempat_lahir': row['tempat_lahir'],
                            'tgl_lahir': row['tgl_lahir'],
                            'jenis_kelamin': row['jenis_kelamin'],
                            'no_hp': row.get('no_hp', ''),
                            'thn_gabung': row.get('thn_gabung'),
                            'provinsi': row.get('provinsi'),
                            'kabupaten': row.get('kabupaten'),
                            'kecamatan': row.get('kecamatan'),
                            'kelurahan': row.get('kelurahan'),
                            'alamat': row.get('alamat'),
                            'perguruan': perguruan,
                            'nama_pelatih': row.get('nama_pelatih'),
                            'unit_latihan': row.get('unit_latihan'),
                            'provinsi_latihan': row.get('provinsi_latihan'),
                            'kabupaten_latihan': row.get('kabupaten_latihan'),
                            'kecamatan_latihan': row.get('kecamatan_latihan'),
                            'kelurahan_latihan': row.get('kelurahan_latihan'),
                            'parent':parent,
                            'ktp':'default.jpeg',
                            'pas_photo':'default.jpeg',
                        }
                    )
                    
                    # Create user account if not exists
                    if not member.user:
                        user, user_created = AccountUser.objects.get_or_create(
                            username=row['nik'],
                            email=row['email'],
                            defaults={
                                'first_name': row['nama'],
                                'role': RoleUser.SANTRI,
                                'kabupaten': row.get('kabupaten'),
                                'wilayah': row.get('kecamatan'),
                            }
                        )
                        if user_created:
                            user.set_password("pagarnusabwi1985.1986")
                            user.save()
                        
                        member.user = user
                        member.save()
                    
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {index + 2}: {str(e)}")  # +2 for header and 0-based index
            
            # Show results to user
            if success_count > 0:
                messages.success(self.request, f"Successfully imported {success_count} members!")
            if error_count > 0:
                messages.warning(self.request, f"Failed to import {error_count} members. See errors below.")
                for error in errors[:10]:  # Show first 10 errors to avoid flooding
                    messages.error(self.request, error)
            
            return super().form_valid(form)
            
        except Exception as e:
            messages.error(self.request, f"Error processing Excel file: {str(e)}")
            return self.form_invalid(form)
        
class DownloadMemberTemplateView(IsPublicAuth, View):
    def get(self, request, *args, **kwargs):
        # Create a sample DataFrame with the required columns
        df = pd.DataFrame(columns=[
            'nik', 'email', 'nama', 'tempat_lahir', 'tgl_lahir', 'jenis_kelamin',
            'no_hp', 'thn_gabung', 'provinsi', 'kabupaten', 'kecamatan', 'kelurahan',
            'alamat', 'perguruan', 'nama_pelatih', 'unit_latihan', 'provinsi_latihan',
            'kabupaten_latihan', 'kecamatan_latihan', 'kelurahan_latihan'
        ])
        
        # Add one sample row
        df.loc[0] = [
            '1234567890123456', 'example@email.com', 'John Doe', 'Jakarta', '1990-01-01', 'L',
            '08123456789', '2023-01-01', 'DKI Jakarta', 'Jakarta Selatan', 'Kebayoran Baru', 'Senayan',
            'Jl. Contoh No. 123', 1, 'Pelatih Name', 'Unit Name', 'Provinsi Latihan', 
            'Kabupaten Latihan', 'Kecamatan Latihan', 'Kelurahan Latihan'
        ]
        
        # Create Excel file in memory
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Members', index=False)
        writer.close()
        output.seek(0)
        
        # Create response
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=member_template.xlsx'
        return response