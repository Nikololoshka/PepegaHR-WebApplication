from os import path

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


def user_photo_path(instance, filename) -> str:
    """
    Путь для сохранения фотографии профиля.
    """
    return f'user-photos/profile_{instance.id}{path.splitext(filename)[1]}'


class HRUser(AbstractUser):
    """
    Объект пользователя с дополнительной информацией (профилем).
    """
    # возможные роли пользователя
    ADMIN_ROLE = 'adm'
    MODERATOR_ROLE = 'mod'
    USER_ROLE = 'usr'

    USER_ROLES = (
        (ADMIN_ROLE, _('Администратор')),
        (MODERATOR_ROLE, _('Модератор')),
        (USER_ROLE, _('Пользователь'))
    )

    photo = models.ImageField(upload_to=user_photo_path, default='user-photos/default.png', blank=True)
    role = models.CharField(max_length=3, choices=USER_ROLES, default='usr', blank=False)
    last_visit = models.DateTimeField(blank=True, null=True)
    departaments = models.ManyToManyField('Departament', blank=True)

    def is_admin(self) -> bool:
        """
        Проверяет, имеет ли пользователь роль администрата.
        """
        return self.role == HRUser.ADMIN_ROLE

    def is_moderator(self) -> bool:
        """
        Проверяет, имеет ли пользователь роль модератора.
        """
        return self.role != HRUser.USER_ROLE

    def is_user(self) -> bool:
        """
        Проверяет, имеет ли пользователь роль пользователя.
        """
        return self.role == HRUser.USER_ROLE

    @staticmethod
    def get_departament_model():
        """
        Возвращает модуль группы.
        """
        return Departament

    def get_full_name_reverse(self) -> str:
        """
        Возвращает полное имя пользователя в обратном порядке.
        """
        return f'{self.last_name} {self.first_name}'

    class Meta:
        managed = True
        verbose_name = 'HRUser'
        verbose_name_plural = 'HRUsers'
        ordering = ['last_name', 'first_name']


class Departament(models.Model):
    """
    Объект отдела для пользователей.
    """
    name = models.CharField(max_length=128, blank=False)

    class Meta:
        managed = True
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']

    def __str__(self):
        return f'"{self.name}"'

# DEBUG
# us = HRUser.objects.get(id=1)
# print(us.username)
# print("Password", us.set_password("admin12345"))
# us.save()