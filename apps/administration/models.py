from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    """
    Объект профиля пользователя. Дополнительная информация.
    """
    departament = models.ForeignKey('Departament', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class HRUser(AbstractUser):
    """
    Объект пользователя с дополнительной информацией (профилем).
    """
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True, null=True)


class Departament(models.Model):
    """
    Объект отдела для пользователей.
    """
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('Departament', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
