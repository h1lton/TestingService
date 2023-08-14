from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import ResultForm, LoginForm, RegisterForm
from .models import Test, Question, Result


class TestListView(ListView):
    model = Test
    template_name = 'tests/list.html'

    def get_queryset(self):
        return Test.objects.annotate(
            num_questions=Count('question', distinct=True),
            num_passed=Count('result', filter=Q(result__user_id=self.request.user.id), distinct=True)).order_by('-id')


@login_required
def test_view(request, test_id):
    results = Result.objects.filter(question__test_id=test_id, user_id=request.user.id)
    passed = results.count()
    questions = Question.objects.filter(test_id=test_id)
    total = questions.count()
    title = Test.objects.get(id=test_id).title
    context = {
        'title': title,
        'total': total,
        'test_id': test_id,
    }

    def _result_view():
        # Показывает результаты.
        _questions = questions.prefetch_related(
            'answer_set',
            'answer_set__result_set'
        ).filter(
            test_id=test_id,
            answer__result__user_id=request.user.id
        )
        _results = results.filter(answer__is_true=True).count()
        _context = {
            'results': _results,
            'questions': _questions
        }
        return render(request, 'tests/results.html', context | _context)

    if passed == total:
        # Был сделан запрос с пройденным тестом.
        return _result_view()

    question = questions[passed]
    form = ResultForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        # Отправили ответ на вопрос.
        Result.objects.update_or_create(
            question=question,
            test_id=test_id,
            user_id=request.user.id,
            defaults={'answer_id': request.POST['answer']}
        )
        return redirect('test', test_id)

    # Не был пройден тест и не отправили результаты поэтому выводим вопрос с вариантами ответов.
    return render(
        request,
        'tests/question.html',
        context | {
            'form': form,
            'question': question,
            'passed': passed,
            'progress': str(passed / total * 100)
        }
    )


"""Блок с пользователями"""


class LoginAndRegisterMixin:

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(LoginAndRegisterMixin, CreateView):
    form_class = RegisterForm
    template_name = 'tests/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginAndRegisterMixin, LoginView):
    form_class = LoginForm
    template_name = 'tests/login.html'

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('home'))


def logout_user(request):
    logout(request)
    return redirect('login')
