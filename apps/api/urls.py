from django.urls import path

from .views import user, login


app_name = "api"
urlpatterns = [
    path('user/', user),
    path('login/', login)
]
