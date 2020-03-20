from os import path

from django.db import models
from django.contrib.auth.models import AbstractUser


def user_photo_path(instance, filename) -> str:
    """
    Путь для сохранения фотографии профиля.
    """
    return f'user-photos/profile_{instance.id}.{path.splitext(filename)[1]}'


class HRUser(AbstractUser):
    """
    Объект пользователя с дополнительной информацией (профилем).
    """
    # возможные роли пользователя
    USER_ROLES = (
        ('adm', 'Администратор'),
        ('mod', 'Модератор'),
        ('usr', 'Пользователь')
    )

    photo = models.ImageField(upload_to=user_photo_path, default='user-photos/default.png')
    role = models.CharField(max_length=3, choices=USER_ROLES, default='usr')
    last_visit = models.DateTimeField(blank=True, null=True)

    def is_moderator(self) -> bool:
        """
        Проверяет, является ли пользователь модератором.
        """
        return self.role == 'mod'

    class Meta:
        managed = True
        verbose_name = 'HRUser'
        verbose_name_plural = 'HRUsers'


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
