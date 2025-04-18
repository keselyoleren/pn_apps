from config.form import AbstractForm
from config.request import get_user
from members.models import IKT, Members, Sertifikat
from django import forms
from django.utils import timezone



class MembersForm(AbstractForm):
    nama_pelatih = forms.ModelChoiceField(
        queryset=Members.objects.filter(is_pelatih=True),
        required=False,
        label="Nama Pelatih",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Members
        fields = '__all__'  


class SuperUserMembersForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuperUserMembersForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            if field == 'created_by' and not get_user().is_superuser:
                self.fields['created_by'].widget = forms.HiddenInput()
            
            if field in ['tgl_lahir', 'thn_gabung', 'tanggal_terbit']:
                current_value = self.initial.get(field, None)
                formatted_value = ''
                if current_value:
                    if isinstance(current_value, str):
                        # If it's already a string, try to parse it
                        try:
                            dt = timezone.datetime.strptime(current_value, '%Y-%m-%d')
                            formatted_value = dt.strftime('%Y-%m-%d')
                        except ValueError:
                            formatted_value = current_value.split(' ')[0]  # Just take date part
                    else:
                        # For datetime/date objects
                        formatted_value = current_value.strftime('%Y-%m-%d')
                
                self.fields[field].widget = forms.DateInput(attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'value': formatted_value
                },format='%Y-%m-%d',)

class IKTForm(AbstractForm):
    status = forms.CharField(widget=forms.HiddenInput(), required=False)
    alasan_penolakan = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = IKT
        fields = '__all__'  

class SuperUserIKTForm(forms.ModelForm):
    class Meta:
        model = IKT
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuperUserIKTForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class SuperUserCertificateForm(forms.ModelForm):
    class Meta:
        model = Sertifikat
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuperUserCertificateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field in ['tgl_lahir', 'thn_gabung', 'tanggal_terbit']:
                current_value = self.initial.get(field, None)
                formatted_value = ''
                if current_value:
                    if isinstance(current_value, str):
                        try:
                            dt = timezone.datetime.strptime(current_value, '%Y-%m-%d')
                            formatted_value = dt.strftime('%Y-%m-%d')
                        except ValueError:
                            formatted_value = current_value.split(' ')[0]  # Just take date part
                    else:
                        formatted_value = current_value.strftime('%Y-%m-%d')
                
                self.fields[field].widget = forms.DateInput(attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'value': formatted_value
                })


class CertificateForm(AbstractForm):
    class Meta:
        model = Sertifikat
        fields = '__all__'