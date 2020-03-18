from django.db import models
from django.contrib.auth.models import AbstractUser


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

    photo = models.ImageField(upload_to='user-photos/', default='user-photos/default.png')
    role = models.CharField(max_length=3, choices=USER_ROLES, default='usr')

    def is_moderator(self):
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
