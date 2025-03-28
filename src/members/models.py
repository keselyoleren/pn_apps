from django.db import models
from config.models import BaseModel
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from users.models import AccountUser

# Create your models here.

class Members(BaseModel):
    user = models.OneToOneField(AccountUser, on_delete=models.CASCADE, blank=True, null=True)
    nik = models.CharField("NIK", max_length=50, unique=True)
    email = models.EmailField("Email", max_length=50, unique=True)
    nama = models.CharField("Nama Lengkap", max_length=200)
    tempat_lahir = models.CharField("Tempat Lahir", max_length=50)
    tgl_lahir = models.DateField("Tanggal Lahir")
    jenis_kelamin = models.CharField("Jenis Kelamin", max_length=10, choices=(('L', 'Laki-laki'), ('P', 'Perempuan')))
    no_hp = models.CharField("No. HP", max_length=20, blank=True, null=True)

    thn_gabung = models.DateField("Tahun bergabung", blank=True, null=True)
    lokasi = models.CharField("Lokasi Latihan", max_length=200, blank=True, null=True)
    provinsi = models.CharField("Provinsi", max_length=100, blank=True, null=True)
    kabupaten = models.CharField("Kabupaten", max_length=100, blank=True, null=True)
    kecamatan = models.CharField("Kecamatan", max_length=100, blank=True, null=True)
    kelurahan = models.CharField("Kelurahan", max_length=100, blank=True, null=True)
    unit_latihan = models.CharField("Unit Latihan", max_length=100, blank=True, null=True)

    pas_photo = models.ImageField("Pas Photo", upload_to="members/pas_photo", blank=True, null=True)
    ktp = models.ImageField("KTP", upload_to="members/ktp", blank=True, null=True)


    class Meta:
        verbose_name = "Anggota"
        verbose_name_plural = "Anggota"

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

        if self.pas_photo:
            image_path = self.pas_photo.path  
            with Image.open(image_path) as img:
                target_size = (354, 354)  
                img = img.resize(target_size, Image.Resampling.LANCZOS)
                img.save(image_path, format="JPEG", quality=95)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        try:
            if self.avatar:
                img = Image.open(self.pas_photo)
                if img.height > 200 or img.width > 200:
                    output_size = (200, 200)
                    img.thumbnail(output_size)
                    img_io = BytesIO()
                    img.save(img_io, format=img.format)
                    self.avatar = InMemoryUploadedFile(img_io,
                        "ImageField",
                        self.avatar.name,
                        f"image/{img.format.lower()}",
                        img_io.getbuffer().nbytes,
                        None,
                    )
                    super().save(*args, **kwargs)  
        except Exception as e:
            print(f"Error processing image: {e}")
    