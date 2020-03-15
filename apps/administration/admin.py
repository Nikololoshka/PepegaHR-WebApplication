from django.contrib import admin

from .models import Departament, HRUser, Profile


admin.site.register(Departament)
admin.site.register(Profile)
admin.site.register(HRUser)
