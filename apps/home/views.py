from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model


from questionnaire.models import Questionnaire


@login_required
@require_GET
def home(request: WSGIRequest):
    """
    Отображает главную страницу в системе.
    """
    HRUser = get_user_model()
    hr_user = get_object_or_404(HRUser, id=request.user.id)

    questionnaires = Questionnaire.objects.filter(is_draft=False, groups__in=hr_user.departaments.all())
    questionnaires = questionnaires.exclude(answers__user=hr_user, answers__is_complete=True)

    return render(request, 'home/base.html', {
        'questionnaires': questionnaires
    })
