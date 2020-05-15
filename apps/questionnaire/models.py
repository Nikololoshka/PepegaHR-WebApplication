from django.db import models
from django.conf import settings
from django.utils import timezone
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
    groups = models.ManyToManyField('administration.Departament', blank=True, related_name='questionnaires')

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


class Answer(models.Model):
    """
    Ответ пользователя на тест.
    """ 
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True)
    step = models.SmallIntegerField(default=0)
    is_complite = models.BooleanField(default=False)

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


class SingleChooseAnswer(models.Model):
    """
    Ответ на вопрос с одним вариантом ответа.
    """
    root = models.ForeignKey('SingleChooseQuiz', on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey('Answer', related_name='single_answers', on_delete=models.CASCADE, null=False)
    order = models.SmallIntegerField(default=-1)
    right = models.OneToOneField('SingleChooseVariant', on_delete=models.SET_NULL, null=True)

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


class MultiChooseAnswerVariant(models.Model):
    """
    Один из вариантов ответа на вопрос с несколькими вариантами ответа.
    """
    answer = models.ForeignKey('MultiChooseAnswer', related_name='variants', on_delete=models.CASCADE, null=False)
    right = models.OneToOneField('MultiChooseVariant', on_delete=models.SET_NULL, null=True)

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

