# polls/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Question, Choice

# Базовая форма для вопроса
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

# Форма для одного варианта ответа
ChoiceFormSet = inlineformset_factory(
    Question,  # Родительская модель
    Choice,    # Дочерняя модель
    fields=['choice_text'],  # Поля из Choice
    extra=3,   # Количество пустых форм для вариантов по умолчанию
    can_delete=True, # Разрешить удаление вариантов
    widgets={'choice_text': forms.TextInput(attrs={'class': 'form-control'})}
)