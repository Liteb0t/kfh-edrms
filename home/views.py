from django.shortcuts import render
# from django.core import serializers
# from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User

from home.forms import *
from home.models import Employee, Document, DocumentAccessRequest, Branch, DocumentAuditTrail
import json
from django.utils import timezone
from guardian.shortcuts import assign_perm
import datetime

import os


@login_required
def index(request):
    #documents = Document.objects.all().values()
    # Filter records where the datetime field falls within a specific range
    start_date = timezone.now() - timezone.timedelta(days=31)
    end_date = timezone.now()
    queryset = (Document.objects.filter(uploaded_at__range=(start_date, end_date))
                .values("id", "title", "uploaded_at", "criticality"))

    # pending = DocumentAccessRequest.objects.all()
    # .values("requested_permission", "request_date", "employee", "document")
    pending = (DocumentAccessRequest.objects
               .filter(request_employees=request.user)
               .filter(pending=True)
               .values("id", "requested_permission", "request_date", "employee", "document"))

    context = {
        'pendingAsJson': json.dumps(list(pending), default=str),
        'documents': queryset,
        'documentsAsJson': json.dumps(list(queryset), default=str),
    }

    return render(request, 'dashboard.html', context)
    #now = datetime.now()
    #today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    #today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    #objects = Document.objects.filter(Q(date__gte=today_min) & Q(date__lte=today_max))


@login_required
def Employees(request):
    employees = Employee.objects.all().values('first_name', 'last_name', 'username', 'email', 'date_joined')
    you = Employee.objects.get(username=request.user.username)
    print(request.user)
    print(request.user.id)
    print(request.user.username)
    context = {
        'employeesAsJson': json.dumps(list(employees), default=str),
        # 'range': range(Employee.objects.all().__len__()),
        'you': you,
    }
    return render(request, 'employees.html', context)


@login_required
def EmployeeDetails(request, username):
    employee = Employee.objects.get(username=username)
    documents_uploaded = (Document.objects.filter(uploaded_by=employee)
                          .values("id", "title", "uploaded_at", "criticality"))
    print("Documents uploaded:", documents_uploaded)
    if not documents_uploaded:
        documents_uploaded = "none"
    else:
        documents_uploaded = json.dumps(list(documents_uploaded), default=str)
    if not employee.last_login:
        employee_last_login = "Never"
    else:
        employee_last_login = employee.last_login
    context = {
        'employee': employee,
        'documents_uploaded': documents_uploaded,
        'employee_last_login': employee_last_login,
    }
    return render(request, 'employee-details.html', context)


@login_required
def Documents(request):
    documents = Document.objects.all().values("id", "title", "uploaded_at", "criticality")
    context = {
        'documents': documents,
        'documentsAsJson': json.dumps(list(documents), default=str),
    }
    return render(request, 'documents.html', context)


@login_required
def RecentlyUploadedDocuments(request):
    documents = (Document.objects.all()
                 .filter(manually_deleted=True)
                 .values("id", "title", "delete_at"))

    start_date = timezone.now() - timezone.timedelta(days=31)
    end_date = timezone.now()
    documents = (Document.objects.filter(uploaded_at__range=(start_date, end_date))
                .values("id", "title", "uploaded_at", "criticality"))

    context = {
        'documents': documents,
        'documentsAsJson': json.dumps(list(documents), default=str),
    }
    return render(request, 'documents-recently-uploaded.html', context)


@login_required
def RecentlyDeletedDocuments(request):
    documents = (Document.objects.all()
                 .filter(manually_deleted=True)
                 .values("id", "title", "delete_at"))
    context = {
        'documents': documents,
        'documentsAsJson': json.dumps(list(documents), default=str),
    }
    return render(request, 'documents-recently-deleted.html', context)


@login_required
def DocumentDetails(request, document_id, messages=None):
    if messages is None:
        messages = []
    document = Document.objects.get(id=document_id)
    if request.user.has_perm("view_document", document) and \
            request.user.has_perm("edit_document", document) and \
            request.user.has_perm("delete_document", document):
        has_all_perms = True
    else:
        has_all_perms = False

    context = {
        'mailto_link': document.uploaded_by.email,
        'has_all_perms': has_all_perms,
        'user_permissions': {
            'view_document': request.user.has_perm("view_document", document),
            # 'add_document': request.user.has_perm("add_document", document),
            'change_document': request.user.has_perm("change_document", document),
            'delete_document': request.user.has_perm("delete_document", document),
        },
        'user': request.user,
        'document': document,
        'messages': messages
    }
    # if document.manually_deleted:
    #     context['messages'] = ["This document has been marked for deletion."]
    return render(request, 'document-details.html', context)


@login_required
def DocumentHistory(request, document_id):
    document = Document.objects.get(id=document_id)
    audit_trail = DocumentAuditTrail.objects.filter(document=document).values("id", "user__username", "action", "timestamp")

    context = {
        'document': document,
        'auditTrailAsJson': json.dumps(list(audit_trail), default=str),
    }
    return render(request, 'document-history.html', context)


def Branches(request):
    branches = Branch.objects.all().values()
    context = {
        'branchesAsJson': json.dumps(list(branches), default=str),
    }
    return render(request, 'branches.html', context)


def BranchDetails(request, branch_id):
    branch = Branch.objects.get(id=branch_id)
    employees_at_this_branch = (Employee.objects.filter(branch_id=branch_id)
                          .values('first_name', 'last_name', 'username', 'email', 'date_joined'))
    print("Documents uploaded:", employees_at_this_branch)
    if not employees_at_this_branch:
        employees_at_this_branch = "none"
    else:
        employees_at_this_branch = json.dumps(list(employees_at_this_branch), default=str)
    context = {
        'branch': branch,
        'employees_at_this_branch': employees_at_this_branch,
    }
    return render(request, 'branch-details.html', context)


@login_required
def BranchEmployees(request, branch_id):
    branch = Branch.objects.get(id=branch_id)
    employees_at_this_branch = (Employee.objects.filter(branch_id=branch_id)
                          .values('first_name', 'last_name', 'username', 'email', 'date_joined'))
    print("Documents uploaded:", employees_at_this_branch)
    if not employees_at_this_branch:
        employees_at_this_branch = "none"
    else:
        employees_at_this_branch = json.dumps(list(employees_at_this_branch), default=str)
    context = {
        'branch': branch,
        'employees_at_this_branch': employees_at_this_branch,
    }
    return render(request, 'branch-employees.html', context)


@login_required
def Upload(request):
    # process uploaded file
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.delete_at = timezone.now() + timezone.timedelta(days=365*7)
            obj.save()
            document = Document.objects.get(id=obj.id)
            assign_perm("view_document", request.user, document)
            assign_perm("change_document", request.user, document)
            assign_perm("delete_document", request.user, document)
            uploaded_audit_entry = DocumentAuditTrail(
                document=document,
                user=request.user,
                action="Upload",
                description="Document uploaded for the first time.")
            uploaded_audit_entry.save()
            return render(request, 'upload.html', {'form': form, 'messages': ["Uploaded successfully"]})
            # return RequestPermissions(request, obj.id)
        else:
            return render(request, 'upload.html', {'form': form, 'messages': ["Upload failed"]})
    else:
        form = DocumentForm()
    # load page normally
    return render(request, 'upload.html', {'form': form})


@login_required
def EditDocument(request, document_id):
    document = Document.objects.get(id=document_id)
    if request.user.has_perm("edit_document", document):
        # process uploaded file
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.uploaded_by = request.user
                obj.save()
                uploaded_audit_entry = DocumentAuditTrail(
                    document=document,
                    user=request.user,
                    action="Edit",
                    description="Document edited because i said so.")
                uploaded_audit_entry.save()
                return render(request, 'upload.html', {'form': form, 'messages': ["Edited successfully"]})
                # return RequestPermissions(request, obj.id)
            else:
                return render(request, 'upload.html', {'form': form, 'messages': ["Edit failed"]})
        else:
            form = DocumentForm(instance=document)
        # load page normally
        return render(request, 'upload.html', {'form': form})
    else:
        return HttpResponseForbidden("You don't have permission to edit this document. Go back and request permissions.")


# @login_required
# def ViewProtectedFile(request, path):
#     # Check user permissions or any other access control logic here
#     if not request.user.has_perm('home.view_document'):
#         return HttpResponseForbidden("You don't have permission to access this media.")
#
#     print("ViewProtectedFile path:", path)
#     # Construct the full path to the media file
#     media_path = os.path.join(settings.MEDIA_ROOT, path)
#
#     # Serve the file
#     with open(media_path, 'rb') as file:
#         response = HttpResponse(file.read(), content_type='application/octet-stream')
#
#     return response


@login_required
def ViewDocument(request, document_id):
    document = Document.objects.get(id=document_id)
    path = document.file.name
    # Check user permissions or any other access control logic here
    if not request.user.has_perm('home.view_document', document):
        return HttpResponseForbidden("You don't have permission to access this media.")

    # Construct the full path to the media file
    media_path = os.path.join(settings.MEDIA_ROOT, path)

    # Can i do this more easily?
    if path.endswith('.pdf'):
        temp_content_type = "application/pdf"
    elif path.endswith('.png'):
        temp_content_type = "image/png"
    elif path.endswith('.jpg'):
        temp_content_type = "image/jpeg"
    else:
        temp_content_type = "application/octet-stream"

    # Serve the file
    with open(media_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=temp_content_type)

    return response


def delete_document(request, document_id):
    document = Document.objects.get(id=document_id)
    if request.user.has_perm('delete_document', document):
        # document.delete()
        document.manually_deleted = True
        document.delete_at = timezone.now() + timezone.timedelta(days=30)
        message = "Document deleted."
    else:
        # return HttpResponseForbidden("You don't have permission to delete this file.")
        message = "You don't have permission to delete this document."

    return DocumentDetails(request, document_id, messages=[message])


@login_required
def RequestPermissions(request, document_id):
    document = Document.objects.get(id=document_id)
    # process uploaded file
    if request.method == 'POST':
        form = DocumentAccessRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee = request.user
            obj.document = document
            obj.save()
            form.save_m2m()
            return index(request)
        else:
            print("something wasnt valid")
    else:
        form = DocumentAccessRequestForm(initial={"supervisor": document.uploaded_by})
    # load page normally
    return render(request, 'request-permissions.html', {'form': form})


@login_required
def ReviewPermissionRequest(request, request_id):
    permission_request = DocumentAccessRequest.objects.get(id=request_id)
    document = permission_request.document
    requester = permission_request.employee
    messages = []

    if request.method == 'POST':
        form = ApproveOrRejectRequest(request.POST)
        if form.is_valid():
            if form.cleaned_data["choice"] == "approve":
                print("FORM APPROVED!!!1!!!")
                if permission_request.requested_permission == "view_document":
                    assign_perm(permission_request.requested_permission, requester, document)
                    message = "Granted view permission"
                elif permission_request.requested_permission == "add_document":
                    message = "Validated uploaded document"
                elif permission_request.requested_permission == "delete_document":
                    # document.delete()
                    document.manually_deleted = True
                    document.delete_at = timezone.now() + timezone.timedelta(days=30)
                    message = "Document deleted"
                else:
                    message = "Form is approved"
                    # return render(request, 'delete_document.html')
            elif form.cleaned_data["choice"] == "reject":

                if permission_request.requested_permission == "add_document":
                    # document.delete()
                    document.manually_deleted = True
                    document.delete_at = timezone.now() + timezone.timedelta(days=30)
                    message = "Upload invalidated. Document deleted"
                else:
                    message = "Permission rejected"
            else:
                message = "Error - Invalid choice"
            if message:
                messages = [message]
            permission_request.pending = False
            permission_request.save()
    else:
        form = ApproveOrRejectRequest()

    return render(request, 'review_permission_request.html',
                  {
                      "document": document,
                      "request": permission_request,
                      "requester": requester,
                      "form": form,
                      "messages": messages,
                  })