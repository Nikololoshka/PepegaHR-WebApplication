from django import forms
from django.forms import formset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone

import locale
from contextlib import contextmanager
from datetime import datetime

from .models import Questionnaire, SingleChooseQuiz, SingleChooseVariant, \
                    MultiChooseQuiz, MultiChooseVariant, ArbitraryQuiz, \
                    SingleChooseAnswer, MultiChooseAnswer, MultiChooseAnswerVariant, ArbitraryAnswer


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
        fields = ['name', 'desciption', 'max_count', 'is_shuffle', 'test_time']

        labels = {
            'name': _('Название'),
            'desciption': _('Описание'),
            'max_count': _('Максимальное количество вопросов'),
            'is_shuffle': _('Перемешивать вопросы'),
            'test_time': _('Время прохождения теста')
        }

        help_texts = {
            'max_count': _('Если не указано, то нет ограничений'),
            'test_time': _('Если не указано, то нет ограничений')
        }


class QuestionnairePublicationForm(forms.ModelForm):
    """
    Форма для публикации теста.
    """
    open_date = forms.CharField(label=_('Дата начала'), required=False)
    open_time = forms.TimeField(label=_('Время начала'), required=False, localize=True)
    close_date = forms.CharField(label=_('Дата конца'), required=False)
    close_time = forms.TimeField(label=_('Время конца'), required=False, localize=True)

    user_id = None

    class Meta:
        model = Questionnaire
        fields = ['groups', 'show_result']
        labels = {
            'groups': _('Группы'),
            'show_result': _('Показать результат пользователю')
        }

    def __init__(self, *args, **kwargs):
        if 'user_id' in kwargs:
            self.user_id = kwargs.pop('user_id')

        super(QuestionnairePublicationForm, self).__init__(*args, **kwargs)
        
        # инициализация списка групп
        # if self.user_id is not None:
        #    HRUser = get_user_model()
        #    hr_user = HRUser.objects.get(id=self.user_id)
        #    self.fields['groups'].queryset = hr_user.departaments.all()

        # инициализация даты и времени
        if self.instance:
            open_datetime = self.instance.open_datetime
            close_datetime = self.instance.close_datetime

            with QuestionnairePublicationForm.rus_locale():
                pattern_date = '%b %d, %Y'
                pattern_time = '%H:%M'

                if open_datetime is not None:
                    open_datetime = open_datetime.astimezone(timezone.get_current_timezone())
                    self.fields['open_date'].initial = open_datetime.strftime(pattern_date).title()
                    self.fields['open_time'].initial = open_datetime.strftime(pattern_time).title()

                if close_datetime is not None:
                    close_datetime = close_datetime.astimezone(timezone.get_current_timezone())
                    self.fields['close_date'].initial = close_datetime.strftime(pattern_date).title()
                    self.fields['close_time'].initial = close_datetime.strftime(pattern_time).title()
 
    @staticmethod
    @contextmanager
    def rus_locale():
        """
        Устанавливает русскую локаль в контекст.
        """
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, 'ru_RU')
        finally:
            locale.setlocale(locale.LC_ALL, saved)

    def clean(self):
        """
        Проверяет форму на правильность.
        """
        cleaned_data = super(QuestionnairePublicationForm, self).clean()

        # проверка дат
        pattern = '%b %d, %Y'
        open_date = self.cleaned_data['open_date']
        close_date = self.cleaned_data['close_date']

        # парсинг с локалью
        with QuestionnairePublicationForm.rus_locale():
            # парсинг начала
            if open_date:
                try:
                    open_date = datetime.strptime(open_date, pattern)
                except ValueError:
                    raise ValidationError(_('Не правильный формат даты: ') + open_date)

            # парсинг конца
            if close_date:
                try:
                    close_date = datetime.strptime(close_date, pattern)
                except ValueError:
                    raise ValidationError(_('Не правильный формат даты: ') + close_date)
        

        if open_date and close_date and open_date > close_date:
            raise ValidationError(_('Дата начала позже даты конца'))

        open_date = open_date if open_date else None
        close_date = close_date if close_date else None

        open_time = self.cleaned_data['open_time']
        close_time = self.cleaned_data['close_time']


        # дата и время
        if (open_date is None) ^ (open_time is None):
            raise ValidationError(_('Дата и время начала заполнены не до конца'))
        else:
            # заполнена дата начала
            if open_date is None and open_time is None:
                open_datetime = None
            else:
                open_datetime = datetime.combine(open_date, open_time)

        if (close_date is None) ^ (close_time is None):
            raise ValidationError(_('Дата и время конца заполнены не до конца'))
        else:
            # заполнена дата конца
            if close_date is None and close_time is None:
                close_datetime = None
            else:
                close_datetime = datetime.combine(close_date, close_time)

        if open_datetime is not None and close_datetime is not None and open_datetime >= close_datetime:
            raise ValidationError(_('Время и дата начала позже времени и даты конца или совпадает'))

        self.cleaned_data['open_datetime_clean'] = open_datetime
        self.cleaned_data['close_datetime_clean'] = close_datetime        

    def save(self, commit=True):
        """
        Сохраняет данные в БД.
        """
        questionnaire = super(QuestionnairePublicationForm, self).save(commit=False)
        
        open_datetime = self.cleaned_data['open_datetime_clean']
        close_datetime = self.cleaned_data['close_datetime_clean']

        questionnaire.open_datetime = open_datetime
        questionnaire.close_datetime = close_datetime

        if commit:
            questionnaire.save()

        return questionnaire


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

        super(SingleChooseForm, self).__init__(*args, **kwargs)
        request = args[0] if len(args) else {}

        # если форма из POST запроса
        if request:
            i = 0
            right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)

            while request.get(variant_field_name):
                right = request.get(right_field_name, None)
                right = (right is not None)

                variant = request[variant_field_name]
                value = request.get(value_field_name, 0)
                self._add_fields(right_field_name, right, value_field_name, value, variant_field_name, variant)

                i += 1
                right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)
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
                    right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)

                    self._add_fields(right_field_name, variants[i] == right, 
                                     value_field_name, variants[i].value,
                                     variant_field_name, variants[i].variant)
            else:
                # extra форма
                self.fields['forms_count'].initial = 1

                right_field_name, value_field_name, variant_field_name = self.get_fields_name(0)

                self._add_fields(right_field_name, False, value_field_name, 0, variant_field_name, '')

    def _add_fields(self, right_field_name: str, right: bool, value_field_name: str, value: int, variant_field_name: str, variant: str):
        """
        Добавляет поля на форму.
        """
        self.fields[right_field_name] = forms.BooleanField(required=False)
        self.initial[right_field_name] = 'on' if right else ''
        
        self.fields[value_field_name] = forms.IntegerField(required=True, min_value=0)
        self.initial[value_field_name] = value

        self.fields[variant_field_name] = forms.CharField(widget=forms.Textarea(), required=True)
        self.initial[variant_field_name] = variant


    def clean(self):
        """
        Проверяет форму на правильность.
        """
        cleaned_data = super(SingleChooseForm, self).clean()

        rights = list()
        values = list()
        variants = list()

        i = 0
        right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)


        while cleaned_data.get(variant_field_name):
            right = cleaned_data.get(right_field_name, None)
            value = cleaned_data.get(value_field_name, 0)

            variant = cleaned_data[variant_field_name]

            if variant in variants:
                raise forms.ValidationError(_('Есть одинаковые поля'))
            else:
                rights.append(right)
                values.append(value)
                variants.append(variant)

            i += 1
            right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)

        if sum(rights) != 1:
            raise ValidationError(_('Должен быть ровно один правильный ответ'))

        if sum(values) < 1:
            raise ValidationError(_('За вопрос нужно получить хотя бы одни балл'))

        self.cleaned_data['rights'] = rights
        self.cleaned_data['values'] = values
        self.cleaned_data['variants'] = variants

    def save(self):
        """
        Сохраняет вопрос в БД.
        """
        quiz = super(SingleChooseForm, self).save(commit=False)
        questionnaire = Questionnaire.objects.get(id=self.questionnaire_id)

        if not hasattr(quiz, 'questionnaire'):
            quiz.questionnaire = questionnaire
            quiz.order = len(questionnaire.get_quizzes_list())
        else:
            quiz.right = None

        quiz.save()
        count = quiz.variants.all().count()
        current_count = 0

        for index, (right, value, variant) in enumerate(zip(self.cleaned_data['rights'], \
                                            self.cleaned_data['values'], self.cleaned_data['variants'])):
            single_variant, _ = SingleChooseVariant.objects.update_or_create(
                quiz=quiz,
                order=index,
                defaults={
                    'variant': variant,
                    'value': value
                }
            )

            if right:
                quiz.right = single_variant

            current_count += 1

        while current_count < count:
            single_variant = SingleChooseVariant.objects.get(quiz=quiz, order=current_count)
            single_variant.delete()

            current_count += 1

        quiz.save()

        questionnaire.modify()
        return quiz

    @staticmethod
    def get_fields_name(index: int):
        """
        Возвращает кортеж из имен полей соответсвующих переданому индексу.
        """
        return f'right-{index}-form', f'value-{index}-form', f'variant-{index}-form'

    def get_fields(self):
        """
        Возвращает список кортежей с полями.
        """
        i = 0
        while True:
            right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)

            if self.fields.get(right_field_name) and self.fields.get(variant_field_name) \
                    and self.fields.get(value_field_name):

                yield self[right_field_name], self[value_field_name], self[variant_field_name]
                i += 1
            else:
                break


class MultiChooseForm(forms.ModelForm):
    """
    Форма для вопроса с одним выбором ответа.
    """
    forms_count = forms.IntegerField(min_value=1, widget=forms.HiddenInput())
    questionnaire_id = None

    class Meta:
        model = MultiChooseQuiz
        fields = ['question']
        labels = {
            'question': _('Вопрос')
        }

    def __init__(self, *args, **kwargs):
        if 'questionnaire_id' in kwargs:
            self.questionnaire_id = kwargs.pop('questionnaire_id')

        super(MultiChooseForm, self).__init__(*args, **kwargs)
        request = args[0] if len(args) else {}


        # если форма из POST запроса
        if request:
            i = 0
            right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)

            while request.get(variant_field_name):
                right = request.get(right_field_name, None)
                right = (right is not None)

                variant = request[variant_field_name]
                value = request.get(value_field_name, 0)
                self._add_fields(right_field_name, right, value_field_name, value, variant_field_name, variant)

                i += 1
                right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)
        else:
            # получения вариантов вопроса
            variants = MultiChooseVariant.objects.filter(
                quiz=self.instance
            )

            if len(variants):       
                # создание полей
                self.fields['forms_count'].initial = len(variants) 
                
                for i in range(len(variants)):
                    right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)

                    self._add_fields(right_field_name, variants[i].right, 
                                     value_field_name, variants[i].value,
                                     variant_field_name, variants[i].variant)
            else:
                # extra форма
                self.fields['forms_count'].initial = 1
                right_field_name, value_field_name, variant_field_name = self.get_fields_name(0)

                self._add_fields(right_field_name, False, value_field_name, 0, variant_field_name, '')

    def _add_fields(self, right_field_name: str, right: bool, value_field_name: str, value: int, variant_field_name: str, variant: str):
        """
        Добавляет поля на форму.
        """
        self.fields[right_field_name] = forms.BooleanField(required=False)
        self.initial[right_field_name] = 'on' if right else ''
        
        self.fields[value_field_name] = forms.IntegerField(required=True, min_value=0)
        self.initial[value_field_name] = value

        self.fields[variant_field_name] = forms.CharField(widget=forms.Textarea(), required=True)
        self.initial[variant_field_name] = variant


    def clean(self):
        """
        Проверяет форму на правильность.
        """
        cleaned_data = super(MultiChooseForm, self).clean()

        rights = list()
        values = list()
        variants = list()

        i = 0
        right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)


        while cleaned_data.get(variant_field_name):
            right = cleaned_data.get(right_field_name, None)
            value = cleaned_data.get(value_field_name, 0)

            variant = cleaned_data[variant_field_name]

            if variant in variants:
                raise forms.ValidationError(_('Есть одинаковые поля'))
            else:
                rights.append(right)
                values.append(value)
                variants.append(variant)

            i += 1
            right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)


        if sum(rights) <= 0:
            raise ValidationError(_('Должен быть хотя бы один правильный ответ'))

        if sum(values) < 1:
            raise ValidationError(_('За вопрос нужно получить хотя бы одни балл'))

        self.cleaned_data['rights'] = rights
        self.cleaned_data['values'] = values
        self.cleaned_data['variants'] = variants

    def save(self):
        """
        Сохраняет вопрос в БД.
        """
        quiz = super(MultiChooseForm, self).save(commit=False)
        questionnaire = Questionnaire.objects.get(id=self.questionnaire_id)

        if not hasattr(quiz, 'questionnaire'):
            quiz.questionnaire = questionnaire
            quiz.order = len(questionnaire.get_quizzes_list())

        quiz.save()
        count = quiz.variants.all().count()
        current_count = 0

        for index, (right, value, variant) in enumerate(zip(self.cleaned_data['rights'], \
                                    self.cleaned_data['values'], self.cleaned_data['variants'])):
            MultiChooseVariant.objects.update_or_create(
                quiz=quiz,
                order=index, 
                defaults={
                    'variant': variant,
                    'value': value,
                    'right': right
                }
            )

            current_count += 1

        while current_count < count:
            multi_variant = MultiChooseVariant.objects.get(quiz=quiz, order=current_count)
            multi_variant.delete()

            current_count += 1

        questionnaire.modify()
        return quiz

    @staticmethod
    def get_fields_name(index: int):
        """
        Возвращает кортеж из имен полей соответсвующих переданому индексу.
        """
        return f'right-{index}-form', f'value-{index}-form', f'variant-{index}-form'

    def get_fields(self):
        """
        Возвращает список кортежей с полями.
        """
        i = 0
        while True:
            right_field_name, value_field_name, variant_field_name = self.get_fields_name(i)

            if self.fields.get(right_field_name) and self.fields.get(variant_field_name) \
                    and self.fields.get(value_field_name):
                    
                yield self[right_field_name], self[value_field_name], self[variant_field_name]
                i += 1
            else:
                break


class ArbitraryQuizForm(forms.ModelForm):
    """
    Форма для вопроса с свободной формой ответа.
    """
    questionnaire_id = None

    class Meta:
        model = ArbitraryQuiz
        fields = ['question']
        labels = {
            'question': _('Вопрос')
        }

    def __init__(self, *args, **kwargs):
        if 'questionnaire_id' in kwargs:
            self.questionnaire_id = kwargs.pop('questionnaire_id')

        super(ArbitraryQuizForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Сохраняет вопрос в БД.
        """
        quiz = super(ArbitraryQuizForm, self).save(commit=False)
        questionnaire = Questionnaire.objects.get(id=self.questionnaire_id)

        if not hasattr(quiz, 'questionnaire'):
            quiz.questionnaire = questionnaire
            quiz.order = len(questionnaire.get_quizzes_list())
        
        if commit:
            quiz.save()

        questionnaire.modify()
        return quiz


class SingleChooseAnswerForm(forms.ModelForm):
    """
    Форма для ответа на вопрос с одним вариантом ответа.
    """

    variants = dict()

    class Meta:
        model = SingleChooseAnswer
        fields = []

    def __init__(self, *args, **kwargs):
        super(SingleChooseAnswerForm, self).__init__(*args, **kwargs)

        answer = self.instance
        for index, quiz_variant in enumerate(answer.root.variants.all()):
            right_field_name, variant_name = self._get_fields_name(index)
            self._add_fields(right_field_name, variant_name, quiz_variant)

    def _add_fields(self, right_field_name: str, variant_name: str, variant):
        """
        Добавляет поля на форму.
        """
        self.fields[right_field_name] = forms.BooleanField(required=False)
        self.variants[variant_name] = variant

    def clean(self):
        """
        Проверяет форму на правильность.
        """
        cleaned_data = super(SingleChooseAnswerForm, self).clean()

        i = 0
        right_field_name, variant_name = self._get_fields_name(i)

        right = None
        while self.fields.get(right_field_name) and self.variants.get(variant_name):
            right_data = cleaned_data.get(right_field_name, None)
            print(right_data)
            if right_data is not None and right_data:
                if right is None:
                    right = self.variants[variant_name]
                else:
                    raise ValidationError(_('Должен быть ровно один ответ'))

            i += 1
            right_field_name, variant_name = self._get_fields_name(i)

        if right is None:
            raise ValidationError(_('Должен быть ровно один ответ'))

        self.cleaned_data['right'] = right
    
    def save(self, commit=True):
        """
        Сохраняет ответ в БД.
        """
        answer = super(SingleChooseAnswerForm, self).save(commit=False)
        answer.right = self.cleaned_data['right']

        if commit:
            answer.save()

        return answer

    @staticmethod
    def _get_fields_name(index: int):
        """
        Возвращает кортеж из имен полей соответсвующих переданому индексу.
        """
        return f'right-{index}-form', f'variant-{index}'

    @staticmethod
    def get_type():
        return 'SINGLE'

    def get_fields(self):
        """
        Возвращает список кортежей с полями.
        """
        i = 0
        while True:
            right_field_name, variant_name = self._get_fields_name(i)

            if self.fields.get(right_field_name) and self.variants.get(variant_name):
                yield self[right_field_name], self.variants[variant_name].variant
                i += 1
            else:
                break


class MultiChooseAnswerForm(forms.ModelForm):
    """
    Форма для ответа на вопрос с несколькими вариантами ответа.
    """

    variants = dict()

    class Meta:
        model = MultiChooseAnswer
        fields = []

    def __init__(self, *args, **kwargs):
        super(MultiChooseAnswerForm, self).__init__(*args, **kwargs)

        answer = self.instance
        for index, quiz_variant in enumerate(answer.root.variants.all()):
            right_field_name, variant_name = self._get_fields_name(index)
            self._add_fields(right_field_name, variant_name, quiz_variant)

    def _add_fields(self, right_field_name: str, variant_name: str, variant):
        """
        Добавляет поля на форму.
        """
        self.fields[right_field_name] = forms.BooleanField(required=False)
        self.variants[variant_name] = variant

    def clean(self):
        """
        Проверяет форму на правильность.
        """
        cleaned_data = super(MultiChooseAnswerForm, self).clean()

        i = 0
        right_field_name, variant_name = self._get_fields_name(i)

        rights = []
        while self.fields.get(right_field_name) and self.variants.get(variant_name):
            right_data = cleaned_data.get(right_field_name, None)
            
            if right_data is not None and right_data:
                rights.append(self.variants[variant_name])

            i += 1
            right_field_name, variant_name = self._get_fields_name(i)

        if not len(rights):
            raise ValidationError(_('Должен быть хотя бы один ответ'))

        self.cleaned_data['rights'] = rights
    
    def save(self, commit=True):
        """
        Сохраняет ответ в БД.
        """
        answer = super(MultiChooseAnswerForm, self).save(commit=False)
        rights = self.cleaned_data['rights']

        for right in rights:
            MultiChooseAnswerVariant.objects.create(
                answer=answer,
                right=right
            )

        if commit:
            answer.save()

        return answer

    @staticmethod
    def _get_fields_name(index: int):
        """
        Возвращает кортеж из имен полей соответсвующих переданому индексу.
        """
        return f'right-{index}-form', f'variant-{index}'

    @staticmethod
    def get_type():
        return 'MULTI'

    def get_fields(self):
        """
        Возвращает список кортежей с полями.
        """
        i = 0
        while True:
            right_field_name, variant_name = self._get_fields_name(i)

            if self.fields.get(right_field_name) and self.variants.get(variant_name):
                yield self[right_field_name], self.variants[variant_name].variant
                i += 1
            else:
                break

class ArbitraryAnswerForm(forms.ModelForm):
    """
    Форма для ответа на вопрос с свободном ответом.
    """
    class Meta:
        model = ArbitraryAnswer
        fields = ['right']
        labels = {
            'right': _('Ответ')
        }
