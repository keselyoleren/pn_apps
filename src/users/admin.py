from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import AccountUser

# Register your models here.
@admin.register(AccountUser)
class UserAdmin(BaseUserAdmin):
    list_display = ('username','email','role', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        (_('Personal info'), {'fields': (
            'first_name', 
            'last_name', 
            'email',
            'wilayah'
            )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
    )

