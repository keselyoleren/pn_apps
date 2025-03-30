import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.choice import RoleUser


# Create your models here.

class AccountUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField("Role", max_length=50, choices=RoleUser.choices, default=RoleUser.ADMIN)
    kabupaten = models.CharField("Kabupaten", max_length=50, blank=True, null=True)
    wilayah = models.CharField("Wilayah", max_length=50, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.username

