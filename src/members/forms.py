from config.form import AbstractForm
from members.models import Members


class MembersForm(AbstractForm):
    class Meta:
        model = Members
        fields = '__all__'