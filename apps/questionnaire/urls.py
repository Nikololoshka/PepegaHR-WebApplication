from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.test, name='questionnaire-test'),
    path('drafts', views.drafts_page, name='questionnaire-drafts-page'),
    path('draft/<int:questionnaire_id>', views.draft_page, name='questionnaire-draft-page'),

    path('draft/<int:questionnaire_id>/single_choose', views.single_choose_page, name='questionnaire-single-choose-create'),
    path('draft/<int:questionnaire_id>/single_choose/<int:quiz_id>', views.single_choose_page, name='questionnaire-single-choose-edit'),
    path('draft/<int:questionnaire_id>/single_choose_remove/<int:quiz_id>', views.single_choose_remove, name='questionnaire-single-choose-remove'),

    path('draft/<int:questionnaire_id>/multi_choose', views.multi_choose_page, name='questionnaire-multi-choose-create'),
    path('draft/<int:questionnaire_id>/multi_choose/<int:quiz_id>', views.multi_choose_page, name='questionnaire-multi-choose-edit'),
    path('draft/<int:questionnaire_id>/multi_choose_remove/<int:quiz_id>', views.multi_choose_remove, name='questionnaire-multi-choose-remove'),

    path('draft/<int:questionnaire_id>/arbitrary', views.arbitrary_page, name='questionnaire-arbitrary-create'),
    path('draft/<int:questionnaire_id>/arbitrary/<int:quiz_id>', views.arbitrary_page, name='questionnaire-arbitrary-edit'),
    path('draft/<int:questionnaire_id>/arbitrary_remove/<int:quiz_id>', views.arbitrary_remove_page, name='questionnaire-arbitrary-remove'),
]
