from django.urls import path

from .views import users, create_user


urlpatterns = [
    path('users', users, name='admin-users-page'),
    path('users/create-user', create_user, name='admin-create-user-page')
]
