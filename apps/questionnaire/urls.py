from django.urls import path, re_path
from . import views


urlpatterns = [
    # publications
    path('publications', views.publications_page, name='questionnaire-publications-page'),

    # drafts
    path('drafts', views.drafts_page, name='questionnaire-drafts-page'),

    # survey
    path('survey/<int:questionnaire_id>', views.survey_page, name='questionnaire-survey-page'),
    path('survey/<int:questionnaire_id>/settings', views.survey_setting_page, name='questionnaire-survey-setting-page'),
    path('survey/<int:questionnaire_id>/publication', views.survey_publication_page, name='questionnaire-survey-publication-page'),
    path('survey/to_draft', views.survey_to_draft, name='questionnaire-survey-to-draft'),
    path('survey/remove', views.survey_remove, name='questionnaire-survey-remove'),
    path('survey/result/<int:questionnaire_id>', views.survey_result_page, name='questionnaire-survey-result-page'),

    path('survey/<int:questionnaire_id>/single_choose', views.single_choose_page, name='questionnaire-single-choose-create'),
    path('survey/<int:questionnaire_id>/single_choose/<int:quiz_id>', views.single_choose_page, name='questionnaire-single-choose-edit'),
    path('survey/<int:questionnaire_id>/single_choose/remove', views.single_choose_remove, name='questionnaire-single-choose-remove'),

    path('survey/<int:questionnaire_id>/multi_choose', views.multi_choose_page, name='questionnaire-multi-choose-create'),
    path('survey/<int:questionnaire_id>/multi_choose/<int:quiz_id>', views.multi_choose_page, name='questionnaire-multi-choose-edit'),
    path('survey/<int:questionnaire_id>/multi_choose/remove', views.multi_choose_remove, name='questionnaire-multi-choose-remove'),

    path('survey/<int:questionnaire_id>/arbitrary', views.arbitrary_page, name='questionnaire-arbitrary-create'),
    path('survey/<int:questionnaire_id>/arbitrary/<int:quiz_id>', views.arbitrary_page, name='questionnaire-arbitrary-edit'),
    path('survey/<int:questionnaire_id>/arbitrary/remove', views.arbitrary_remove_page, name='questionnaire-arbitrary-remove'),

    # reports
    path('reports', views.reports_page, name='questionnaire-reports-page'),

    # mytests
    path('mytests', views.mytests_page, name='questionnaire-my-tests-page'),
    path('mytests/review/<int:questionnaire_id>', views.test_review_page, name='questionnaire-review-page'),
    path('mytests/passage/<int:questionnaire_id>', views.test_passage_page, name='questionnaire-passage-page'),
    path('mytests/passage_end/<int:questionnaire_id>', views.test_passage_end_page, name='questionnaire-passage-end-page'),
    path('mytests/passage_result/<int:questionnaire_id>', views.test_passage_result_page, name='questionnaire-passage-result-page')
]
