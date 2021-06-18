from django import forms
from django.contrib.auth.forms import UsernameField

class ResultForm(forms.Form):
    username = UsernameField(
        label='Student ID',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
