from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.views.generic import TemplateView
from config.choice import RoleUser
from config.permis import IsPublicAuth, IsLoginAuthenticated, LoginRequiredMixin
from members.forms import MembersForm
from members.models import Members
from users.models import AccountUser
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


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
        member, created = AccountUser.objects.get_or_create(
            username=email, 
            role=RoleUser.MEMBER,
            defaults={'email': email}
        )
        self.object.member = member
        self.object.save()
        messages.success(self.request, "Anggota berhasil didaftarkan hubungi admin wilayah untuk pengecekan dan setting password!")
        return response

class MembersListView(IsPublicAuth, ListView):
    model = Members
    template_name = 'members/list.html'
    context_object_name = 'list_members'
    
    def get_queryset(self):
        user_wilayah = self.request.user.wilayah
        if self.request.user.is_superuser:
            return Members.objects.all()
        if self.request.user.role == RoleUser.MEMBER:
            return Members.objects.filter(user=self.request.user)
        return Members.objects.filter(kecamatan=user_wilayah)

    
    def get_context_data(self, **kwargs):
        if self.request.user.role == RoleUser.MEMBER:
            context = super().get_context_data(**kwargs)
            context['header'] = 'Data diri'
            context['header_title'] = 'Data diri'
            context['btn_add'] = False
        else:
            context = super().get_context_data(**kwargs)
            context['header'] = 'Member'
            context['header_title'] = 'List Member'
            context['btn_add'] = True
            context['create_url'] = reverse_lazy('member-create')
        return context


class MembersUpdateView(IsPublicAuth, UpdateView):
    model = Members
    template_name = 'component/form.html'
    form_class = MembersForm
    success_url = reverse_lazy('member-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == RoleUser.MEMBER:
            context['header'] = 'Data diri'
            context['header_title'] = 'Edit data diri'
        else:
            context['header'] = 'Member'
            context['header_title'] = 'Edit Member'
        return context

class MembersDeleteView(IsPublicAuth, DeleteView):
    model = Members
    template_name = 'component/delete.html'
    success_url = reverse_lazy('member-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Member'
        context['header_title'] = 'Delete Member'
        return context
