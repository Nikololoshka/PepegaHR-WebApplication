from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path(r'^users$', views.users_page, name='admin-users-page'),
    path('users/create-user', views.create_user_page, name='admin-create-user-page'),
    path('users/create-user-model', views.create_user_model, name='admin-create-user'),
    path('users/edit-user/<int:user_id>', views.edit_user_page, name='admin-edit-user-page'),
    path('users/edit-user-model/<int:user_id>', views.edit_user_model, name='admin-edit-user'),
    path('users/remove-user', views.remove_user_model, name='admin-remove-user'),
]
