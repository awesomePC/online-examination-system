from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from core.models import Exam
from .models import *
from .utils import *

# action strings
ADD_ADMIN = "AA"
REMOVE_ADMIN = "RA"
ADD_TEACHER = "AT"
REMOVE_TEACHER = "RT"
ACTIVATE_ACCOUNT = "AAc"
DEACTIVATE_ACCOUNT = "DAc"

# map actions
ACTIONS = {
    ADD_ADMIN: lambda r, qs: add_to_group(r, qs, "admin"),
    REMOVE_ADMIN: lambda r, qs: remove_from_group(r, qs, "admin"),
    ADD_TEACHER: lambda r, qs: add_to_group(r, qs, "teacher"),
    REMOVE_TEACHER: lambda r, qs: remove_from_group(r, qs, "teacher"),
    ACTIVATE_ACCOUNT: activate_account,
    DEACTIVATE_ACCOUNT: deactivate_account,
}

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


class ActionForm(forms.Form):
    ACTION_CHOICES = [
        (ADD_ADMIN, "Add admin"),
        (REMOVE_ADMIN, "Remove admin"),
        (ADD_TEACHER, "Add teacher"),
        (REMOVE_TEACHER, "Remove teacher"),
        (ACTIVATE_ACCOUNT, "Activate account"),
        (DEACTIVATE_ACCOUNT, "Deactivate account"),
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES, initial=ADD_TEACHER)
