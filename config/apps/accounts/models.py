from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, verbose_name='Отасининг исми', blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Телефон рақами', blank=True, null=True)
    address = models.TextField(verbose_name='Манзил', blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', verbose_name='Фойдаланувчи расми', blank=True, null=True)
    job_position = models.CharField(max_length=100, verbose_name='Лавозими', blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Туғилган санаси', blank=True, null=True)
    date_joined_company = models.DateField(verbose_name='Ишга қабул қилинган сана', blank=True, null=True)
    is_verified = models.BooleanField(default=False, verbose_name='Тасдиқланган аккаунт')
    notes = models.TextField(verbose_name='Қўшимча изоҳлар', blank=True, null=True)

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()
        return full_name if full_name else self.username
