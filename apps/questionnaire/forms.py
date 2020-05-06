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
    Форма для вопроса с одним выбором ответа.
    """
    forms_count = forms.IntegerField(min_value=1, widget=forms.HiddenInput())
    questionnaire_id = None
    
    class Meta:
        model = SingleChooseQuiz
        fields = ['question']
        labels = {
            'question': _('Вопрос')
        }

    def __init__(self, *args, **kwargs):
        if 'questionnaire_id' in kwargs:
            self.questionnaire_id = kwargs.pop('questionnaire_id')

        super().__init__(*args, **kwargs)
        request = args[0] if len(args) else {}


        # если форма из POST запроса
        if request:
            i = 0
            right_field_name = f'right-{i}-form'
            variant_field_name = f'variant-{i}-form'

            while request.get(variant_field_name):
                right = request.get(right_field_name, None)
                right = (1 if right is not None else 0)

                variant = request[variant_field_name]
                self._add_fields(right_field_name, right, variant_field_name, variant)

                i += 1
                right_field_name = f'right-{i}-form'
                variant_field_name = f'variant-{i}-form'
        else:
            # получения вариантов вопроса
            variants = SingleChooseVariant.objects.filter(
                quiz=self.instance
            )

            if len(variants):       
                # создание полей
                self.fields['forms_count'].initial = len(variants) 
                right = self.instance.right
                
                for i in range(len(variants)):
                    right_field_name = f'right-{i}-form'
                    variant_field_name = f'variant-{i}-form'

                    self._add_fields(right_field_name, variants[i] == right, variant_field_name, variants[i])
            else:
                # extra форма
                self.fields['forms_count'].initial = 1

                right_field_name = f'right-0-form'
                variant_field_name = f'variant-0-form'

                self._add_fields(right_field_name, False, variant_field_name, '')

    def _add_fields(self, right_field_name: str, right: bool, variant_field_name: str, variant: str):
        """
        Добавляет пля на форму.
        """
        self.fields[right_field_name] = forms.BooleanField(required=False)
        self.initial[right_field_name] = 'on' if right else ''
        
        self.fields[variant_field_name] = forms.CharField(widget=forms.Textarea(), required=True)
        self.initial[variant_field_name] = variant


    def clean(self):
        """
        Проверяет форму на правильность.
        """
        cleaned_data = super(SingleChooseForm, self).clean()

        rights = list()
        variants = list()

        i = 0
        right_field_name = f'right-{i}-form'
        variant_field_name = f'variant-{i}-form'


        while cleaned_data.get(variant_field_name):
            right = cleaned_data.get(right_field_name, None)

            variant = cleaned_data[variant_field_name]

            if variant in variants:
                raise forms.ValidationError(_('Есть одинаковые поля'))
            else:
                rights.append(right)
                variants.append(variant)

            i += 1
            right_field_name = f'right-{i}-form'
            variant_field_name = f'variant-{i}-form'

        print(rights)
        if sum(rights) != 1:
            raise ValidationError(_('Должен быть ровно один правильный ответ'))

        self.cleaned_data['rights'] = rights
        self.cleaned_data['variants'] = variants

    def save(self):
        """
        Сохраняет вопрос в БД.
        """
        quiz = super(SingleChooseForm, self).save(commit=False)
        questionnaire = Questionnaire.objects.get(id=self.questionnaire_id)
        quiz.questionnaire = questionnaire
        quiz.order = len(questionnaire.get_quizzes_list())
        quiz.variants.all().delete()
        quiz.save()

        for index, (right, variant) in enumerate(zip(self.cleaned_data['rights'], self.cleaned_data['variants'])):
           single_variant = SingleChooseVariant.objects.create(
               quiz=quiz,
               variant=variant,
               order=index
           )
           if right:
                quiz.right = single_variant

        quiz.save()

        return quiz

    def get_fields(self):
        """
        Возвращает список кортежей с полями.
        """
        i = 0
        while True:
            right_field_name = f'right-{i}-form'
            variant_field_name = f'variant-{i}-form'

            if self.fields.get(right_field_name) and self.fields.get(variant_field_name):
                yield self[right_field_name], self[variant_field_name]
                i += 1
            else:
                break

