from django import forms
from home.models import Document, DocumentAccessRequest, Employee, DocumentAuditTrail
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


# class AuditEntryReason(forms.ModelForm):
#
#     description = forms.CharField(widget=forms.Textarea)
#     class Meta:
#         model = DocumentAuditTrail
#         fields = ['description']


class DocumentAccessRequestForm(forms.ModelForm):
    reason_given = forms.CharField(widget=forms.Textarea)
    request_employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all())
    class Meta:
        model = DocumentAccessRequest
        fields = ['reason_given', 'requested_permission', 'request_groups', 'request_employees']


class ApproveOrRejectRequest(forms.Form):
    choices = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    choice = forms.ChoiceField(choices=choices)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = ("email", "first_name", "last_name")
