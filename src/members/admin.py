from django.contrib import admin

from members.models import Members

# Register your models here.
@admin.register(Members)
class AdminMember(admin.ModelAdmin):
    list_display = ('nik', 'nama', 'email', 'tgl_lahir', 'jenis_kelamin', 'no_hp')
    search_fields = ('nik', 'nama', 'email')
    list_filter = ('jenis_kelamin',)

    fieldsets = (
        (None, {
            'fields': ('user', 'nik', 'email', 'nama', 'tempat_lahir', 'tgl_lahir', 'jenis_kelamin', 'no_hp')
        }),
        ('Lokasi', {
            'fields': ('lokasi', 'provinsi', 'kabupaten', 'kecamatan', 'kelurahan', 'unit_latihan')
        }),
        ('Dokumen', {
            'fields': ('pas_photo', 'ktp')
        })
    )
    ordering = ('-created_at',)

    