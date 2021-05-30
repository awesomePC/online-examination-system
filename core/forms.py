from django import forms
from .models import Exam, MCQ

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'active']


class MCQForm(forms.ModelForm):
    class Meta:
        model = MCQ
        fields = [
            'question',
            'answer',
            'option_A',
            'option_B',
            'option_C',
            'option_D',
        ]
