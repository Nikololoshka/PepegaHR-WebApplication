from django import forms
from django.forms import formset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Questionnaire, SingleChooseQuiz, SingleChooseVariant


class SimpleQuestionnaireForm(forms.ModelForm):
    """
    Форма для создания теста.
    """
    class Meta:
        model = Questionnaire
        fields = ['name']

        labels = {
            'name': _('Название')
        }

class QuestionnaireEditForm(forms.ModelForm):
    """
    Форма для редактировния теста.
    """
    class Meta:
        model = Questionnaire
        fields = ['name', 'desciption', 'max_count', 'is_shuffle']

        labels = {
            'name': _('Название'),
            'desciption': _('Описание'),
            'max_count': _('Максимальное количество вопросов'),
            'is_shuffle': _('Перемешивать вопросы')
        }

        help_texts = {
            'max_count': _('Если не указано, то нет ограничений')
        }


class SingleChooseForm(forms.ModelForm):
    """
    Форма для редактирование (создания) теста с одним вариантом ответа
    """
    class Meta:
        model = SingleChooseQuiz
        fields = ['question']
        labels = {
            'question': _('Вопрос')
        }


class SingleChooseVariantForm(forms.ModelForm):
    """
    Набор форм для теста с одним вариантом ответа
    """
    right = forms.BooleanField(required=False)

    class Meta:
        model = SingleChooseVariant
        fields = ['variant']
        
        
class SingleChooseVariantValidation(forms.BaseModelFormSet):
    """
    Валидар для набора форм теста с одним вариантом ответа.
    """
    def clean(self):
        super(SingleChooseVariantValidation, self).clean()

        count = 0
        for form in self.forms:
            if 'right' in form.cleaned_data:
                count += int(form.cleaned_data['right'])

        if count != 1:
            raise ValidationError(_('Должен быть ровно один правильный ответ'))

SingleChooseFormset = modelformset_factory(SingleChooseVariant, form=SingleChooseVariantForm, 
                        formset=SingleChooseVariantValidation, extra=1, min_num=1, can_order=True, can_delete=True)
