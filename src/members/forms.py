from config.form import AbstractForm
from members.models import Members
from django import forms



class MembersForm(AbstractForm):
    class Meta:
        model = Members
        fields = '__all__'  # or specify your fields
    