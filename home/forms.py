from django import forms
from home.models import Document, DocumentAccessRequest, Employee
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
    # uploaded_by = forms.Textarea(disabled=True, required=False)
    class Meta:
        model = Document
        fields = ['title', 'file', 'criticality']


# class DocumentAccessRequestForm(forms.ModelForm):
#     def __init__(self, **kwargs):
#         self.document = kwargs.pop('document', None)
#         self.employee = kwargs.pop('employee', None)
#         super(DocumentAccessRequestForm, self).__init__(**kwargs)
#
#     class Meta:
#         model = DocumentAccessRequest
