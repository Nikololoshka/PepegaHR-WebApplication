from django.urls import path

from . import views


urlpatterns = [
    path('quick_start', views.quick_start_page, name='help-quick-page'),
    path('administration', views.administration_page, name='help-administration-page'),
    path('questionnaire', views.questionnaire_page, name='help-questionnaire-page')
]
