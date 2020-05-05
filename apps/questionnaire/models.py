from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Questionnaire(models.Model):
    """
    Модель опроса (теста).
    """   
    name = models.CharField(max_length=128)
    desciption = models.TextField(blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    max_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=None, blank=True, null=True)
    is_shuffle = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)

    class Meta:
        managed = True
        verbose_name = 'Questionnaire'
        verbose_name_plural = 'Questionnaires'


class SingleChooseQuiz(models.Model):
    """
    Модель вопроса с одним вариантом ответа.
    """  
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    question = models.TextField(max_length=512)
    right = models.SmallIntegerField(default=0)

    class Meta:
        managed = True
        verbose_name = 'SingleChooseQuiz'
        verbose_name_plural = 'SingleChooseQuizzes'


class SingleChooseVariant(models.Model):
    """
    Вариант вопроса с одним вариантом ответа.
    """  
    quiz = models.ForeignKey('SingleChooseQuiz', on_delete=models.CASCADE)
    variant = models.TextField(max_length=256, blank=True)
    order = models.SmallIntegerField(default=0, db_index=True)

    class Meta:
        managed = True
        verbose_name = 'SingleChooseVariant'
        verbose_name_plural = 'SingleChooseVariants'
        ordering = ['order', 'variant']


class MultiChooseeQuiz(models.Model):
    """
    Модель вопроса с множеством вариантов ответа.
    """  
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    question = models.TextField(max_length=512)

    class Meta:
        managed = True
        verbose_name = 'MultiChooseeQuiz'
        verbose_name_plural = 'MultiChooseeQuizzes'


class MultiChooseeVariant(models.Model):
    """
    Вариант вопроса с множеством вариантов ответа.
    """  
    quiz = models.ForeignKey('MultiChooseeQuiz', on_delete=models.CASCADE)
    variant = models.CharField(max_length=128)

    class Meta:
        managed = True
        verbose_name = 'MultiChooseeVariant'
        verbose_name_plural = 'MultiChooseeVariants'


class ArbitraryQuiz(models.Model):
    """
    Модель вопроса с свободном ответом.
    """  
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    question = models.TextField(max_length=512)

    class Meta:
        managed = True
        verbose_name = 'ArbitraryQuiz'
        verbose_name_plural = 'ArbitraryQuizzes'
