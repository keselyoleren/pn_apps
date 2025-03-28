from webbrowser import get
from django import forms
from config.choice import RoleUser
from django.contrib.admin.widgets import (
    FilteredSelectMultiple,
    AdminDateWidget,
    AdminSplitDateTime,
)
from config.request import get_user

class AbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            if field == 'created_by' and not get_user().is_superuser:
                self.fields['created_by'].widget = forms.HiddenInput()
            
            if field in ['tgl_lahir']:
                self.fields['tgl_lahir'].widget = forms.DateTimeInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })

            if field in ['thn_gabung']:
                self.fields['thn_gabung'].widget = forms.DateTimeInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })
            if field in ['user']:
                self.fields['user'].widget = forms.HiddenInput()

