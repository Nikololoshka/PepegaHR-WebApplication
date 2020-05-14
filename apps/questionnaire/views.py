from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .forms import SimpleQuestionnaireForm, QuestionnaireEditForm, QuestionnairePublicationForm, \
                   SingleChooseForm, MultiChooseForm, ArbitraryQuizForm
from .models import Questionnaire, SingleChooseQuiz, MultiChooseQuiz, ArbitraryQuiz

from .permissions import check_ability

from apps.administration.permissions import required_moderator


@login_required
@required_moderator
@require_GET
def publications_page(request: WSGIRequest):
    """
    Отображает список всех опубликованных тестов.
    """
    questionnaires = Questionnaire.objects.filter(is_draft__exact=False)
    
    page_num = request.GET.get('page', 1)
    paginator = Paginator(questionnaires, 30)
    page = paginator.get_page(page_num)

    return render(request, 'questionnaire/publications.html', {
        'page': page
    })


@login_required
@required_moderator
@require_http_methods(['GET', 'POST'])
def drafts_page(request: WSGIRequest):
    """
    GET: отображает список всех черновиков
    POST: создает новый черновик теста
    """
    if request.method == 'POST':
        # получение формы
        form = SimpleQuestionnaireForm(request.POST)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            questionnaire.author = request.user
            questionnaire.save()

            return redirect('questionnaire-survey-page', questionnaire_id=questionnaire.id)

    else:
        form = SimpleQuestionnaireForm()

    questionnaires = Questionnaire.objects.filter(is_draft__exact=True)
    
    page_num = request.GET.get('page', 1)
    paginator = Paginator(questionnaires, 30)
    page = paginator.get_page(page_num)

    return render(request, 'questionnaire/drafts.html', {
        'questionnaire_form': form,
        'page': page
    })


@login_required
@required_moderator
@require_GET
def survey_page(request: WSGIRequest, questionnaire_id: int):
    """
    Отображает текущий черновик теста.
    """
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)

    return render(request, 'questionnaire/survey.html', {
        'questionnaire': questionnaire,
        'quizzes': questionnaire.get_quizzes_list(),
        'SINGLE_QUIZ': Questionnaire.SINGLE_QUIZ,
        'MULTI_QUIZ': Questionnaire.MULTI_QUIZ,
        'ARBITRARY_QUIZ': Questionnaire.ARBITRARY_QUIZ
    })


@login_required
@required_moderator
@require_http_methods(['GET', 'POST'])
def survey_setting_page(request: WSGIRequest, questionnaire_id: int):
    """
    Редактирует тест.
    """
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)

    if request.method == 'POST':
        # получение формы
        form = QuestionnaireEditForm(request.POST, instance=questionnaire)
        if form.is_valid():
            form.save()

            return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)

    else:
        form = QuestionnaireEditForm(instance=questionnaire)

    return render(request, 'questionnaire/survey_setting.html', {
        'form': form,
        'questionnaire': questionnaire
    })


@login_required
@required_moderator
@require_http_methods(['GET', 'POST'])
def survey_publication_page(request: WSGIRequest, questionnaire_id: int):
    """
    Настраивает тест для публикации.
    """
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    publish_errors = None

    if request.method == 'POST':
        # получение формы
        form = QuestionnairePublicationForm(request.POST, instance=questionnaire, user_id=request.user.id)

        if form.is_valid():
            form.save()
            form.save_m2m()

            if request.POST.get('publish', None) is not None:
                # сохраняем и публикуем
                questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
                if questionnaire.open_datetime is not None and questionnaire.close_datetime is not None and questionnaire.groups.exists():
                    questionnaire.is_draft = False
                    questionnaire.save()

                    return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)
                else:
                    publish_errors = [_('Не заполнены все необходимые поля для публикации')]

            else:
                return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)

    else:
        form = QuestionnairePublicationForm(instance=questionnaire, user_id=request.user.id)

    return render(request, 'questionnaire/survey_publication.html', {
        'form': form,
        'publish_errors': publish_errors,
        'questionnaire': questionnaire
    })


@login_required
@required_moderator
@require_POST
def survey_to_draft(request: WSGIRequest):
    """
    Переводит тест в состояние "Черновик".
    """
    questionnaire_id = request.POST.get('questionnaire_id', None)
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    questionnaire.is_draft = True
    questionnaire.save()

    return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)


@login_required
@required_moderator
@require_POST
def survey_remove(request: WSGIRequest):
    """
    Удаляет тест и связанные с ним вопросы.
    """
    questionnaire_id = request.POST.get('questionnaire_id', None)
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    questionnaire.delete()

    return redirect('questionnaire-drafts-page')


@login_required
@required_moderator
@require_http_methods(['GET', 'POST'])
def single_choose_page(request: WSGIRequest, questionnaire_id: int, quiz_id: int = None):
    """
    Создает (редактирует) вопрос с одним вариантом выбора ответа для теста.
    """
    instance = get_object_or_404(SingleChooseQuiz, id=quiz_id) if quiz_id is not None else None

    if request.method == 'POST':
        # получение формы
        form = SingleChooseForm(request.POST, instance=instance, questionnaire_id=questionnaire_id)
        if form.is_valid():
            form.save()

            return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)

    else:
        form = SingleChooseForm(instance=instance)

    return render(request, 'questionnaire/quiz/single_quiz.html', {
        'form': form,
        'quiz_id': quiz_id,
        'questionnaire_id': questionnaire_id,
        'action': _('Добавить') if instance is None else _('Изменить'),
        'title_action': _('Создание') if instance is None else _('Редактирование')
    })


@login_required
@required_moderator
@require_POST
def single_choose_remove(request: WSGIRequest, questionnaire_id: int):
    """
    Удаляет вопрос с одним вариантом ответа из теста.
    """
    quiz_id = request.POST.get('quiz_id', None)
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    quiz = get_object_or_404(questionnaire.single_quizzes, id=quiz_id)

    quiz.delete()
    questionnaire.recompute_order()

    return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)
    

@login_required
@required_moderator
@require_http_methods(['GET', 'POST'])
def multi_choose_page(request: WSGIRequest, questionnaire_id: int, quiz_id: int = None):
    """
    Создает (редактирует) вопрос с множестов вариантов выбора ответа для теста.
    """
    instance = get_object_or_404(MultiChooseQuiz, id=quiz_id) if quiz_id is not None else None

    if request.method == 'POST':
        # получение формы
        form = MultiChooseForm(request.POST, instance=instance, questionnaire_id=questionnaire_id)
        if form.is_valid():
            form.save()

            return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)

    else:
        form = MultiChooseForm(instance=instance)

    return render(request, 'questionnaire/quiz/multi_quiz.html', {
        'form': form,
        'quiz_id': quiz_id,
        'questionnaire_id': questionnaire_id,
        'action': _('Добавить') if instance is None else _('Изменить'),
        'title_action': _('Создание') if instance is None else _('Редактирование')
    })


@login_required
@required_moderator
@require_POST
def multi_choose_remove(request: WSGIRequest, questionnaire_id: int):
    """
    Удаляет вопрос с множестов вариантов выбора из теста.
    """
    quiz_id = request.POST.get('quiz_id', None)
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    quiz = get_object_or_404(questionnaire.multi_quizzes, id=quiz_id)

    quiz.delete()
    questionnaire.recompute_order()

    return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)


@login_required
@required_moderator
@require_http_methods(['GET', 'POST'])
def arbitrary_page(request: WSGIRequest, questionnaire_id: int, quiz_id: int = None):
    """
    Создает (редактирует) вопрос с свободном вариантом ответа для теста.
    """
    instance = get_object_or_404(ArbitraryQuiz, id=quiz_id) if quiz_id is not None else None

    if request.method == 'POST':
        # получение формы
        form = ArbitraryQuizForm(request.POST, instance=instance, questionnaire_id=questionnaire_id)
        if form.is_valid():
            form.save()

            return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)

    else:
        form = ArbitraryQuizForm(instance=instance)

    return render(request, 'questionnaire/quiz/arbitrary_quiz.html', {
        'form': form,
        'quiz_id': quiz_id,
        'questionnaire_id': questionnaire_id,
        'action': _('Добавить') if instance is None else _('Изменить'),
        'title_action': _('Создание') if instance is None else _('Редактирование')
    })


@login_required
@required_moderator
@require_POST
def arbitrary_remove_page(request: WSGIRequest, questionnaire_id: int):
    """
    Удаляет вопрос с свободной формой из теста.
    """
    quiz_id = request.POST.get('quiz_id', None)
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    quiz = get_object_or_404(questionnaire.arbitrary_quizzes, id=quiz_id)

    quiz.delete()
    questionnaire.recompute_order()

    return redirect('questionnaire-survey-page', questionnaire_id=questionnaire_id)


@login_required
@required_moderator
def reports_page(request: WSGIRequest):
    return render(request, 'questionnaire/reports.html')


@login_required
@require_GET
def mytests_page(request: WSGIRequest):
    """
    Отображает список доступных мне тестов.
    """
    HRUser = get_user_model()
    hr_user = get_object_or_404(HRUser, id=request.user.id)

    questionnaires = Questionnaire.objects.filter(is_draft__exact=False, groups__in=hr_user.departaments.all())

    return render(request, 'questionnaire/mytests.html', {
        'questionnaires': questionnaires
    })


@login_required
@require_http_methods(['GET', 'POST'])
def test_review_page(request: WSGIRequest, questionnaire_id: int):
    """
    Просмотр теста для пользователя.
    """
    hr_user, questionnaire = check_ability(request.user.id, questionnaire_id)

    return render(request, 'questionnaire/review.html', {
        'questionnaire': questionnaire
    })


@login_required
@require_http_methods(['GET', 'POST'])
def test_passage_page(request: WSGIRequest, questionnaire_id: int):
    """
    Прохождение теста.
    """
    hr_user, questionnaire = check_ability(request.user.id, questionnaire_id)

    return render(request, 'questionnaire/passage.html', {
        'questionnaire': questionnaire
    })
    
