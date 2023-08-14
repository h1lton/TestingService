from django.contrib.auth.models import User
from django.db import models


class Test(models.Model):
    title = models.CharField('название', max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['-id']


class Question(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    question = models.CharField('вопрос', max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Набор')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    answer = models.CharField('ответ', max_length=255)
    is_true = models.BooleanField('правильный')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')

    def __str__(self):
        return f'{self.user}-{self.test}-{self.question}-{self.answer}'

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
