from django.urls import path

from . import views


urlpatterns = [
    path('', views.profile_page, name='profile-page'),
    path('edit', views.profile_edit, name='profile-edit'),
]
