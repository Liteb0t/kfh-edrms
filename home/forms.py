from django import forms
from home.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']