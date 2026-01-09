from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    # Основное поле для вопроса
    # pub_date можно добавить автоматически или скрытым полем

    # Дополнительное поле НЕ из модели. Для ввода вариантов ответа.
    choices_text = forms.CharField(
        label='Варианты ответов (каждый с новой строки)',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        help_text='Введите каждый вариант ответа на отдельной строке.'
    )

    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
        }