from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .forms import QuestionForm
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
import requests
import json


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
            Return the last five published questions (not including those set to be
            published in the future).
            """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

@login_required
def question_new(request):
    if request.method == "POST":
        # Пользователь отправил форму
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 1. Сначала сохраняем вопрос (но не в БД, пока)
            question = form.save(commit=False)
            # 2. Если у модели Question есть pub_date, установим его
            question.pub_date = timezone.now()
            # 3. Если есть связь с пользователем (author):
            # question.author = request.user
            # 4. Сохраняем вопрос в БД
            question.save()

            # 5. Обрабатываем варианты ответов из текстового поля
            choices_text = form.cleaned_data['choices_text']
            # Разбиваем текст по строкам, убираем пустые
            choice_list = [line.strip() for line in choices_text.split('\n') if line.strip()]

            for choice_text in choice_list:
                # Создаем объект Choice для каждого варианта
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    votes=0
                )

            # Перенаправляем на страницу деталей созданного опроса
            return redirect('polls:detail', pk=question.id)
    else:
        # Пользователь просто зашел на страницу, показываем пустую форму
        form = QuestionForm()

    return render(request, 'polls/question_edit.html', {'form': form})

def search_polls(request):
    """Страница поиска опросов с аналитикой"""
    return render(request, 'polls/search.html')

def poll_analytics(request, question_id):
    """Страница аналитики для конкретного опроса"""
    context = {
        'question_id': question_id,
    }
    return render(request, 'polls/analytics.html', context)