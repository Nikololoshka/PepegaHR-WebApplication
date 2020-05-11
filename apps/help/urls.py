from django.urls import path

from . import views


urlpatterns = [
    path('quick_start', views.quick_start_page, name='help-quick-page')
]
