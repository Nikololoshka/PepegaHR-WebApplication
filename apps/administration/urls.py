from django.urls import path, re_path

from . import views


urlpatterns = [
    path('users', views.users_page, name='admin-users-page'),
    path('users/hr-user', views.hr_user_page, name='admin-user-create'),
    path('users/hr-user/<int:user_id>', views.hr_user_page, name='admin-user-edit'),
    path('users/remove-user', views.remove_user, name='admin-user-remove'),

    path('departaments', views.departaments_page, name='admin-departaments-page'),
    path('departaments/<int:departament_id>', views.departament_page, name='admin-departament-page'),
    path('departaments/<int:departament_id>/remove-user', views.departament_remove_user, name='admin-departament-user-remove'),
    path('departaments/<int:departament_id>/remove', views.departament_remove, name='admin-departament-remove'),
    
    path('information', views.information_page, name='admin-information-page'),
]
