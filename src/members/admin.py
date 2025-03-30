from django.contrib import admin

from members.models import IKT, Members, Sertifikat

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

    
@admin.register(IKT)
class IKTAdmin(admin.ModelAdmin):
    pass
    # list_display = ('members', 'status', 'alasan_penolakan')
    # search_fields = ('members__nama', 'members__nik')
    # list_filter = ('status',)

    # fieldsets = (
    #     (None, {
    #         'fields': ('members', 'status', 'alasan_penolakan')
    #     }),
    # )
    # ordering = ('-created_at',)

@admin.register(Sertifikat)
class SertifikatAdmin(admin.ModelAdmin):
    pass
    # list_display = ('members', 'sertifikat')
    # search_fields = ('members__nama', 'members__nik')
    # list_filter = ('sertifikat',)

    # fieldsets = (
    #     (None, {
    #         'fields': ('members', 'sertifikat')
    #     }),
    # )
    # ordering = ('-created_at',)