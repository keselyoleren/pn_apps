
from rest_framework import serializers

from manage_users.models import AccountUser

class UserSerialize(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = ('id', 'username', 'email')