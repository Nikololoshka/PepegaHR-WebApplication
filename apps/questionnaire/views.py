from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.utils.translation import gettext_lazy as _

from .forms import SimpleQuestionnaireForm, QuestionnaireEditForm, SingleChooseForm, MultiChooseForm, ArbitraryQuizForm
from .models import Questionnaire, SingleChooseQuiz, MultiChooseQuiz, ArbitraryQuiz

from apps.administration.permissions import required_moderator


@login_required
@required_moderator
def test(request: WSGIRequest):
    return render(request, 'questionnaire/test.html', {
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

            return redirect('questionnaire-draft-page', questionnaire_id=questionnaire.id)

    else:
        form = SimpleQuestionnaireForm()

    questionnaires = Questionnaire.objects.all()

    page_num = request.GET.get('page', 1)
    paginator = Paginator(questionnaires, 30)
    page = paginator.get_page(page_num)

    return render(request, 'questionnaire/drafts.html', {
        'questionnaire_form': form,
        'page': page
    })


@login_required
@required_moderator
@require_http_methods(['GET', 'POST'])
def draft_page(request: WSGIRequest, questionnaire_id: int):
    """
    Отображает текущий черновик теста.
    """
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)

    if request.method == 'POST':
        form = QuestionnaireEditForm(request.POST, instance=questionnaire)
        if form.is_valid():
            questionnaire = form.save()
            form = QuestionnaireEditForm(instance=questionnaire)

    else:
        form = QuestionnaireEditForm(instance=questionnaire)

    return render(request, 'questionnaire/draft.html', {
        'form': form,
        'questionnaire': questionnaire,
        'quizzes': questionnaire.get_quizzes_list(),
        'SINGLE_QUIZ': Questionnaire.SINGLE_QUIZ,
        'MULTI_QUIZ': Questionnaire.MULTI_QUIZ,
        'ARBITRARY_QUIZ': Questionnaire.ARBITRARY_QUIZ
    })


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

            return redirect('questionnaire-draft-page', questionnaire_id=questionnaire_id)

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
def single_choose_remove(request: WSGIRequest, questionnaire_id: int, quiz_id: int):
    """
    Удаляет вопрос с одним вариантом ответа из теста.
    """
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    quiz = get_object_or_404(questionnaire.single_quizzes, id=quiz_id)

    quiz.delete()
    questionnaire.recompute_order()

    return redirect('questionnaire-draft-page', questionnaire_id=questionnaire_id)
    

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

            return redirect('questionnaire-draft-page', questionnaire_id=questionnaire_id)

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
def multi_choose_remove(request: WSGIRequest, questionnaire_id: int, quiz_id: int):
    """
    Удаляет вопрос с множестов вариантов выбора из теста.
    """
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    quiz = get_object_or_404(questionnaire.multi_quizzes, id=quiz_id)

    quiz.delete()
    questionnaire.recompute_order()

    return redirect('questionnaire-draft-page', questionnaire_id=questionnaire_id)


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

            return redirect('questionnaire-draft-page', questionnaire_id=questionnaire_id)

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
def arbitrary_remove_page(request: WSGIRequest, questionnaire_id: int, quiz_id: int):
    """
    Удаляет вопрос с свободной формой из теста.
    """
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    quiz = get_object_or_404(questionnaire.arbitrary_quizzes, id=quiz_id)

    quiz.delete()
    questionnaire.recompute_order()

    return redirect('questionnaire-draft-page', questionnaire_id=questionnaire_id)
