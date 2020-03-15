from django.db import models
from django.db.models import Manager


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    objects = Manager()
