from random import choice

from tests.models import *
from django.db import connection


# from terminal_assistant import *


def time_of_function(function):
    def wrapped(*args):
        start_time = time.perf_counter_ns()
        res = function(*args)
        final_time = time.perf_counter_ns() - start_time
        print("{:,}".format(final_time))
        return res

    return wrapped


@time_of_function
def create_tests(name, i):
    lst_tests = []
    lst_question = []
    lst_answers = []

    for num in range(1, i + 1):
        lst_tests.append(Test(title=f'{name} {num}'))

    Test.objects.bulk_create(lst_tests)

    for test in lst_tests:
        lst_question.append(Question(question=f'Вопрос 1', test=test))
        lst_question.append(Question(question=f'Вопрос 2', test=test))

    Question.objects.bulk_create(lst_question)

    for question in lst_question:
        lst_answers.append(Answer(answer=f'Ответ 1', is_true=False, question=question))
        lst_answers.append(Answer(answer='Ответ 2', is_true=True, question=question))

    Answer.objects.bulk_create(lst_answers)
    print('Success')


@time_of_function
def create_test(name, num_question, num_answer):
    lst_question = []
    lst_answers = []

    test = Test.objects.create(title=name)

    for i in range(1, num_question + 1):
        lst_question.append(Question(question=f'Вопрос {i}', test=test))

    Question.objects.bulk_create(lst_question)

    for question in lst_question:
        for i in range(1, num_answer):
            lst_answers.append(Answer(answer=f'Ответ {i}', is_true=False, question=question))
        lst_answers.append(Answer(answer=f'Ответ {num_answer}', is_true=True, question=question))

    Answer.objects.bulk_create(lst_answers)
    print('Success')
    return test


def print_questions_and_results(test_id, user_id):
    questions = Question.objects.prefetch_related('answer_set', 'answer_set__result_set').filter(test_id=test_id, answer__result__user_id=user_id)
    for question in questions:
        print(question)
        for answer in question.answer_set.all():
            s = 'Неправильный'
            if answer.is_true:
                s = 'Правильный'
            if answer.result_set.exists():
                print(f'\t{s} - {answer} - выбран')
            else:
                print(f'\t{s} - {answer}')


def create_results(test_id, user_id):
    Result.objects.filter(test_id=test_id, user_id=user_id).delete()
    questions = Question.objects.filter(test_id=test_id).prefetch_related('answer_set')
    lst_results = []
    for question in questions:
        lst_results.append(
            Result(
                answer=choice(question.answer_set.all()),
                user_id=user_id,
                question=question,
                test_id=test_id
            )
        )
    Result.objects.bulk_create(lst_results)
    print('Success')


def get_admin():
    return User.objects.get(username='admin')


def create_admin():
    user = User.objects.create_superuser('admin', password='admin')
    print('Success')
    return user


def num_queries():
    return len(connection.queries)
