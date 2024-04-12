from django import forms
from home.models import Document, Employee
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = ("email", "first_name", "last_name")
