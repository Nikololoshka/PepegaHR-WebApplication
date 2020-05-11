from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

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
    groups = models.ManyToManyField('administration.Departament', blank=True)

    class Meta:
        managed = True
        verbose_name = 'Questionnaire'
        verbose_name_plural = 'Questionnaires'
        ordering = ['name', 'desciption']

    def get_quizzes_list(self) -> list:
        """
        Возвращает список вопрос в тесте по порядку.
        """
        return sorted(itertools.chain.from_iterable([
            list(self.single_quizzes.all()), 
            list(self.multi_quizzes.all()), 
            list(self.arbitrary_quizzes.all())
        ]), key=lambda x: x.order)

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
    variant = models.TextField(max_length=256, blank=False)
    order = models.SmallIntegerField(default=-1, db_index=True)

    class Meta:
        managed = True
        verbose_name = 'SingleChooseVariant'
        verbose_name_plural = 'SingleChooseVariants'
        ordering = ['order', 'variant']


class MultiChooseQuiz(models.Model):
    """
    Модель вопроса с множеством вариантов ответа.
    """  
    questionnaire = models.ForeignKey('Questionnaire', related_name='multi_quizzes', on_delete=models.CASCADE)
    question = models.TextField(max_length=512)
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
    variant = models.CharField(max_length=128)
    order = models.SmallIntegerField(default=-1, db_index=True)
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
