from django.utils import timezone
from django import forms
from config.request import get_user

class AbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            if field == 'created_by' and not get_user().is_superuser:
                self.fields['created_by'].widget = forms.HiddenInput()
            
            if field in ['tgl_lahir', 'thn_gabung', 'tanggal_terbit']:
                # Get the current value
                current_value = self.initial.get(field, None)
                
                # Format the date for HTML5 input
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
                }, format='%Y-%m-%d')

            if field in ['user']:
                self.fields['user'].widget = forms.HiddenInput()

