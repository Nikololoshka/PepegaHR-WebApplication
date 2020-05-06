from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.test, name='questionnaire-test'),
    path('drafts', views.drafts_page, name='questionnaire-drafts-page'),
    path('draft/<int:questionnaire_id>', views.draft_page, name='questionnaire-draft-page'),

    path('draft/<int:questionnaire_id>/single_choose_create/', views.single_choose_create_page, name='questionnaire-single-choose-create')
]
