from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .forms import SimpleQuestionnaireForm, QuestionnaireEditForm, SingleChooseForm, SingleChooseFormset
from .models import Questionnaire


@login_required
def test(request: WSGIRequest):
    if request.method == 'POST':
        formset = SingleChooseFormset(request.POST)
        form = SingleChooseForm(request.POST)

        if formset.is_valid() and form.is_valid():
            print('Correct')
        else:
            print(formset.errors)
            print(formset.non_form_errors())
            print(form.errors)

    main_form = QuestionnaireEditForm()

    form = SingleChooseForm()
    formset = SingleChooseFormset()

    return render(request, 'questionnaire/test.html', {
        'form': main_form,
        'main_form': form,
        'formset': formset
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
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    form = QuestionnaireEditForm(instance=questionnaire)

    return render(request, 'questionnaire/draft.html', {
        'form': form
    })