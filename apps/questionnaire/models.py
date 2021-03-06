from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Max

import itertools


class Questionnaire(models.Model):
    """
    Модель опроса (теста).
    """   
    SINGLE_QUIZ = 'single_quiz'
    MULTI_QUIZ = 'multi_quiz'
    ARBITRARY_QUIZ = 'arbitrary_quiz'

    name = models.CharField(max_length=128)
    desciption = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    max_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=None, blank=True, null=True)
    is_shuffle = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    test_time = models.TimeField(blank=True, null=True)

    open_datetime = models.DateTimeField(null=True)
    close_datetime = models.DateTimeField(null=True)
    show_result = models.BooleanField(default=True)
    groups = models.ManyToManyField('administration.Departament', blank=True, related_name='questionnaires')

    class Meta:
        managed = True
        verbose_name = 'Questionnaire'
        verbose_name_plural = 'Questionnaires'
        ordering = ['name', 'desciption']

    def modify(self):
        """
        Вызывается, когда тест был обновлен.
        """
        self.modify_date = timezone.now() 
        self.save()

    def get_quizzes_list(self) -> list:
        """
        Возвращает список вопрос в тесте по порядку.
        """
        return sorted(itertools.chain.from_iterable([
            list(self.single_quizzes.all()), 
            list(self.multi_quizzes.all()), 
            list(self.arbitrary_quizzes.all())
        ]), key=lambda x: x.order)

    def is_wait(self):
        """
        Возвращает True, если тест ожидает открытия для прохождения, иначе False.
        Если не инициализированы даты, то None.
        """
        if self.open_datetime is not None:
            return self.open_datetime > timezone.now() 

        return None

    def is_open(self):
        """
        Возвращает True, если тест открыт для прохождения, иначе False.
        Если не инициализированы даты, то None.
        """
        if self.open_datetime is not None and self.close_datetime is not None:
            now = timezone.now()
            return self.open_datetime < now and now < self.close_datetime

        return None

    def is_close(self):
        """
        Возвращает True, если тест закрыт для прохождения, иначе False.
        Если не инициализированы даты, то None.
        """
        if self.close_datetime is not None:
            return self.close_datetime < timezone.now() 

        return None

    def recompute_order(self):
        """
        Перевычисляет порядок вопросов в тесте.
        """
        for order, quiz in enumerate(self.get_quizzes_list()):
            quiz.order = order
            quiz.save()


class SingleChooseQuiz(models.Model):
    """
    Модель вопроса с одним вариантом ответа.
    """  
    questionnaire = models.ForeignKey('Questionnaire', related_name='single_quizzes', on_delete=models.CASCADE)
    question = models.TextField(max_length=512)
    order = models.SmallIntegerField(default=-1)
    right = models.OneToOneField('SingleChooseVariant', on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = True
        verbose_name = 'SingleChooseQuiz'
        verbose_name_plural = 'SingleChooseQuizzes'

    @staticmethod
    def get_quiz_type() -> str:
        """
        Возвращает тип теста.
        """
        return Questionnaire.SINGLE_QUIZ


class SingleChooseVariant(models.Model):
    """
    Вариант вопроса с одним вариантом ответа.
    """  
    quiz = models.ForeignKey('SingleChooseQuiz', related_name='variants', on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0, null=False)
    variant = models.TextField(max_length=256, default='', blank=False)
    order = models.SmallIntegerField(db_index=True)

    class Meta:
        managed = True
        verbose_name = 'SingleChooseVariant'
        verbose_name_plural = 'SingleChooseVariants'
        ordering = ['order', 'variant']


class MultiChooseQuiz(models.Model):
    """
    Модель вопроса с множеством вариантов ответа.
    """  
    # SUM_METHOD = 'sum'
    # SCALE_METHOD = 'scl'

    # METHODS = (
    #     (SUM_METHOD, _('Суммирование')),
    #     (SCALE_METHOD, _('Масштабирование'))
    # )

    questionnaire = models.ForeignKey('Questionnaire', related_name='multi_quizzes', on_delete=models.CASCADE)
    question = models.TextField(max_length=512)
    # method = models.CharField(default=SUM_METHOD, max_length=3, choices=METHODS, null=False)
    # scale_value = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)], null=False)
    order = models.SmallIntegerField(default=-1)

    class Meta:
        managed = True
        verbose_name = 'MultiChooseQuiz'
        verbose_name_plural = 'MultiChooseQuizzes'
    
    @staticmethod
    def get_quiz_type() -> str:
        """
        Возвращает тип теста.
        """
        return Questionnaire.MULTI_QUIZ


class MultiChooseVariant(models.Model):
    """
    Вариант вопроса с множеством вариантов ответа.
    """  
    quiz = models.ForeignKey('MultiChooseQuiz', related_name='variants', on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0, null=False)
    variant = models.TextField(max_length=256, default='', blank=False)
    order = models.SmallIntegerField(db_index=True)
    right = models.BooleanField(default=False)

    class Meta:
        managed = True
        verbose_name = 'MultiChooseVariant'
        verbose_name_plural = 'MultiChooseVariants'
        ordering = ['order', 'variant']


class ArbitraryQuiz(models.Model):
    """
    Модель вопроса с свободном ответом.
    """  
    questionnaire = models.ForeignKey('Questionnaire', related_name='arbitrary_quizzes', on_delete=models.CASCADE)
    question = models.TextField(max_length=512)
    order = models.SmallIntegerField(default=-1)

    class Meta:
        managed = True
        verbose_name = 'ArbitraryQuiz'
        verbose_name_plural = 'ArbitraryQuizzes'

    @staticmethod
    def get_quiz_type() -> str:
        """
        Возвращает тип теста.
        """
        return Questionnaire.ARBITRARY_QUIZ


class Answer(models.Model):
    """
    Ответ пользователя на тест.
    """ 
    questionnaire = models.ForeignKey('Questionnaire', related_name='answers', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True)
    step = models.SmallIntegerField(default=0)
    is_complete = models.BooleanField(default=False)

    evaluation = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    max_evaluation = models.SmallIntegerField(null=True)

    class Meta:
        managed = True
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def get_quizzes_list(self) -> list:
        """
        Возвращает список вопрос в ответе по порядку.
        """
        return sorted(itertools.chain.from_iterable([
            list(self.single_answers.all()), 
            list(self.multi_answers.all()), 
            list(self.arbitrary_answers.all())
        ]), key=lambda x: x.order)

    def get_evaluation(self, force=False):
        """
        Возвращает оценку за тест.
        """
        if self.evaluation is not None and self.max_evaluation is not None and not force:
            return f'{self.evaluation}/{self.max_evaluation}'

        current_evaluation = 0
        max_evaluation = 0

        answers = self.get_quizzes_list()
        for answer in answers:
            quiz_type = answer.root.get_quiz_type()

            if quiz_type == Questionnaire.SINGLE_QUIZ:
                if answer.right is not None:
                    current_evaluation += answer.right.value

                max_evaluation += answer.root.variants.aggregate(max=Max('value'))['max']
                
            elif quiz_type == Questionnaire.MULTI_QUIZ:
                results = answer.get_rights()
                
                for right_answer, right_my, variant in results:
                    if right_answer:
                         max_evaluation += variant.value
                         if right_my:
                             current_evaluation += variant.value

        self.evaluation = current_evaluation 
        self.max_evaluation = max_evaluation
        self.save()

        return f'{self.evaluation}/{self.max_evaluation}'


class SingleChooseAnswer(models.Model):
    """
    Ответ на вопрос с одним вариантом ответа.
    """
    root = models.ForeignKey('SingleChooseQuiz', on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey('Answer', related_name='single_answers', on_delete=models.CASCADE, null=False)
    order = models.SmallIntegerField(default=-1)
    right = models.ForeignKey('SingleChooseVariant', on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = True
        verbose_name = 'SingleChooseAnswer'
        verbose_name_plural = 'SingleChooseAnswers'


class MultiChooseAnswer(models.Model):
    """
    Ответ на вопрос с несколькими вариантами ответа.
    """
    root = models.ForeignKey('MultiChooseQuiz', on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey('Answer', related_name='multi_answers', on_delete=models.CASCADE, null=False)
    order = models.SmallIntegerField(default=-1)

    class Meta:
        managed = True
        verbose_name = 'MultiChooseAnswer'
        verbose_name_plural = 'MultiChooseAnswers'

    def get_rights(self):
        result = []
        
        variants = self.root.variants.all()
        my_answers = self.variants.values_list('right', flat=True)

        for variant in variants:
            if variant.right:
                if variant.id in my_answers:
                    result.append([True, True, variant])
                else:
                    result.append([True, False, variant])
            else:
                if variant.id in my_answers:
                    result.append([False, True, variant])
                else:
                    result.append([False, False, variant])

        return result

class MultiChooseAnswerVariant(models.Model):
    """
    Один из вариантов ответа на вопрос с несколькими вариантами ответа.
    """
    answer = models.ForeignKey('MultiChooseAnswer', related_name='variants', on_delete=models.CASCADE, null=False)
    right = models.ForeignKey('MultiChooseVariant', on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = True
        verbose_name = 'MultiChooseAnswerVariant'
        verbose_name_plural = 'MultiChooseAnswerVariants'


class ArbitraryAnswer(models.Model):
    """
    Ответ на вопрос с свободном вариантом ответа.
    """
    root = models.ForeignKey('ArbitraryQuiz', on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey('Answer', related_name='arbitrary_answers', on_delete=models.CASCADE, null=False)
    order = models.SmallIntegerField(default=-1)
    right = models.TextField(max_length=512)

    class Meta:
        managed = True
        verbose_name = 'ArbitraryAnswer'
        verbose_name_plural = 'ArbitraryAnswers'

