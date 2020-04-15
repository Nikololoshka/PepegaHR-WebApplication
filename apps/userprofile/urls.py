from django.urls import path

from . import views


urlpatterns = [
    path('', views.my_profile_page, name='my-profile'),
    path('<int:user_id>', views.profile_page, name='profile-page'),
]
