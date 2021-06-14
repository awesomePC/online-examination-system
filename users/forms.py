from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField
)
from core.models import Exam
from .utils import *

# action strings
ADD_ADMIN = 'AA'
REMOVE_ADMIN = 'RA'
ADD_TEACHER = 'AT'
REMOVE_TEACHER = 'RT'
ACTIVATE_ACCOUNT = 'AAc'
DEACTIVATE_ACCOUNT = 'DAc'

# map actions
ACTIONS = {
    ADD_ADMIN: lambda r, qs: add_to_group(r, qs, 'admin'),
    REMOVE_ADMIN: lambda r, qs: remove_from_group(r, qs, 'admin'),
    ADD_TEACHER: lambda r, qs: add_to_group(r, qs, 'teacher'),
    REMOVE_TEACHER: lambda r, qs: remove_from_group(r, qs, 'teacher'),
    ACTIVATE_ACCOUNT: activate_account,
    DEACTIVATE_ACCOUNT: deactivate_account,
}

class StaffRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentRegisterForm(forms.Form):
    file = forms.FileField(
        label='CSV File',
        help_text=(
            '<ul>'
            '<li>Size must be less than 2.5 MB.</li>'
            '<li>Must be a csv file.</li>'
            '<li>Must have "student id" & "email" columns.</li>'
            '</ul>'
            'PLEASE DOUBLE CHECK THE FILE BEFORE PROCEDING, '
            'THE FILE WILL BE ASSUMED TO HAVE NO ERRORS.'
        )
    )


class StudentLoginForm(AuthenticationForm):
    username = UsernameField(
        label='Student ID',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class ExamChoiceForm(forms.Form):
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.filter(active=True),
        to_field_name='name'
    )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ActionForm(forms.Form):
    ACTION_CHOICES = [
        (ADD_ADMIN, 'Add admin'),
        (REMOVE_ADMIN, 'Remove admin'),
        (ADD_TEACHER, 'Add teacher'),
        (REMOVE_TEACHER, 'Remove teacher'),
        (ACTIVATE_ACCOUNT, 'Activate account'),
        (DEACTIVATE_ACCOUNT, 'Deactivate account'),
    ]

    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        initial=ADD_TEACHER
    )
