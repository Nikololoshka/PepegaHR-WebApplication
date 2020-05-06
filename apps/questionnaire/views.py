from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .forms import SimpleQuestionnaireForm, QuestionnaireEditForm, SingleChooseForm
from .models import Questionnaire, SingleChooseQuiz


@login_required
def test(request: WSGIRequest):

    return render(request, 'questionnaire/test.html', {
    })


@login_required
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
@require_http_methods(['GET', 'POST'])
def draft_page(request: WSGIRequest, questionnaire_id: int):
    """
    Отображает текущий черновик теста.
    """
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)

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
@require_http_methods(['GET', 'POST'])
def single_choose_create_page(request: WSGIRequest, questionnaire_id: int):
    """
    Создает вопрос с одним вариантом выбора ответа для теста.
    """
    if request.method == 'POST':
        # получение формы
        form = SingleChooseForm(request.POST, questionnaire_id=questionnaire_id)
        if form.is_valid():
            form.save()

            return redirect('questionnaire-draft-page', questionnaire_id=questionnaire_id)

        else:
            print(form.errors)

    else:
        form = SingleChooseForm()

    return render(request, 'questionnaire/single_choose_create.html', {
        'form': form,
        'questionnaire_id': questionnaire_id
    })