from django.db.models import TextChoices

class RoleUser(TextChoices):
    ADMIN = 'admin'
    SANTRI = 'santri'
    PELATIH = 'pelatih'
    PAC = 'pac'
    PC = 'pc'
    
class Tingkat(TextChoices):
    PUTIH  = 'putih'
    KUNING = 'kuning'
    MERAH = 'merah'
    BIRU = 'biru'
    COKLAT = 'coklat'
    HITAM = 'hitam'

class Status(TextChoices):
    MENUNGGU = 'menunggu'
    DISETUJUI_ADMIN_WILAYAH = 'disetujui admin wilayah'
    DISETUJUI_ADMIN_PAC = 'disetujui admin pac'
    DITOLAK = 'ditolak'