from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

from .models import Questionnaire


def check_ability(user_id, questionnaire_id):
    HRUser = get_user_model()

    hr_user = get_object_or_404(HRUser, id=user_id)
    hr_user_groups = hr_user.departaments.all()

    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, is_draft=False)
    questionnaire_groups = questionnaire.groups.all()

    if not hr_user_groups & questionnaire_groups:
        raise PermissionDenied()

    return hr_user, questionnaire
    
