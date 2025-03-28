import email
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from manage_users.models import AccountUser, Puskeswan



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class RegisterSerialize(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    name =  serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)
    puskeswanCode = serializers.CharField(required=False, allow_blank=True)

    # class Meta:
    #     model = AccountUser
    #     fields = "__all__"

    def validate_puskeswanCode(self, value):
        if not value:
            raise serializers.ValidationError(_('Puskeswan Code is required..!'))
        if value:
            puskeswan = Puskeswan.objects.filter(code=value).first()
            if not puskeswan:
                raise serializers.ValidationError(_("Puskeswan Code not found.!"))
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(_('Email is required..!'))
        if AccountUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email already exists.!"))
        if AccountUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("Username / Email already exists.!"))
        return value
        

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError(_('Password is required..!'))

        if len(value) < 8:
            raise serializers.ValidationError(
                _("Password should be atleast 8 characters long.")
            )
        return value


# {
#     "name": "test",
#     "email": "tetm@gmail.com",
#     "password": "12345678",
#     "puskeswan_code": "12345678"
# }