from django.urls import path, re_path

from . import views


urlpatterns = [
    path('users', views.users_page, name='admin-users-page'),
    path('users/create-user', views.create_user_page, name='admin-user-create'),
    path('users/edit-user/<int:user_id>', views.edit_user_page, name='admin-user-edit'),
    path('users/remove-user', views.remove_user, name='admin-user-remove'),
    path('departaments', views.departaments_page, name='admin-departaments-page'),
    path('information', views.information_page, name='admin-information-page'),
]
