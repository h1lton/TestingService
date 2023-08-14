from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from .models import Answer, Question, Test


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct = True
        not_correct = True
        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data['is_true']:
                    correct = False
                else:
                    not_correct = False
        if correct:
            raise ValidationError('Выберите хотя-бы один верный ответ')
        if not_correct:
            raise ValidationError('Выберите хотя-бы один не верный ответ')


class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 0
    min_num = 2
    formset = AnswerInlineFormSet
    classes = ('inline',)


class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 0
    min_num = 1


@admin.register(Test)
class TestAdmin(NestedModelAdmin):
    list_display = ('title',)
    inlines = [QuestionInline]
