from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    ma_kh = models.CharField(max_length=10, blank=True, null=True)  # ✅ Cần dòng này

    def __str__(self):
        return f"{self.user.username}"
