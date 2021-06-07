from django import forms
from .models import Exam, Question

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'active']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question',
            'correct_answer',
            'option_A',
            'option_B',
            'option_C',
            'option_D',
        ]
