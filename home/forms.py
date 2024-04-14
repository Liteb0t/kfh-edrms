from django import forms
from home.models import Document, Employee
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class DocumentForm(forms.ModelForm):
    # defining criticality choices
    CRITICALITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    #add criticality field to form
    criticality = forms.ChoiceField(choices=CRITICALITY_CHOICES, label='Criticality')
    class Meta:
        model = Document
        fields = ['title', 'file', 'criticality']

#
# class CustomUserCreationForm(UserCreationForm):
#
#     class Meta:
#         model = Employee
#         fields = ("email", "first_name", "last_name")
#
#
# class CustomUserChangeForm(UserChangeForm):
#
#     class Meta:
#         model = Employee
#         fields = ("email", "first_name", "last_name")
