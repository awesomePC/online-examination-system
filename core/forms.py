from django import forms
from .models import Exam, Question


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["name", "duration", "passing_percentage", "active", "show_result"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question",
            "correct_answer",
            "option_A",
            "option_B",
            "option_C",
            "option_D",
            "marks_on_correct_answer",
            "marks_on_wrong_answer",
        ]
        widgets = {"question": forms.Textarea(attrs={"rows": 5})}
