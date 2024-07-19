from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_shoper = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):  # AVAILALBE USER TO ADMIN PANEL
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveBigIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.phone_number} - {self.code}"
