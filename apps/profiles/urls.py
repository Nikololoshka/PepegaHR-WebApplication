from django.urls import path

from . import views


urlpatterns = [
    path('profile/', views.my_profile_page, name='my-profile'),
    path('profile/<int:user_id>', views.profile_page, name='profile-page'),
    path('departament/<int:departament_id>', views.departament_page, name='departament-page')
]
