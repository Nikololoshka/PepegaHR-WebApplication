from django.urls import path

from . import views


urlpatterns = [
    path('users', views.users_page, name='admin-users-page'),
    path('users/create-user', views.create_user_page, name='admin-create-user-page'),
    path('users/create-user-model', views.create_user, name='admin-create-user'),
]
