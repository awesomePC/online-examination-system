from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Exam
from .models import *

ACCOUNT_TYPE_CHOICES = (
    ("S", "Student"),
    ("T", "Teacher"),
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES, widget=forms.RadioSelect()
    )

    class Meta:
        model = User
        fields = ("account_type", "username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email")


class StudentForm(forms.ModelForm):
    standard = forms.CharField(disabled=True)
    branch = forms.CharField(disabled=True)
    division = forms.CharField(disabled=True)
    roll_no = forms.CharField(disabled=True)

    class Meta:
        model = Student
        exclude = ("user",)


class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        exclude = ("user",)


class TeacherForm(forms.ModelForm):
    standard = forms.CharField(disabled=True)
    branch = forms.CharField(disabled=True)
    division = forms.CharField(disabled=True)

    class Meta:
        model = Teacher
        exclude = ("user",)


class TeacherRequestForm(forms.ModelForm):
    class Meta:
        model = TeacherRequest
        exclude = ("user",)
