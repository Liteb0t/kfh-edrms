from django.shortcuts import render
# from django.core import serializers
# from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User

from home.forms import *
from home.models import Employee, Document, DocumentAccessRequest
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
    queryset = Document.objects.filter(uploaded_at__range=(start_date, end_date)).values()
    #my_dictionary = {}

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
        'range': range(Document.objects.all().__len__()),
        #'testdataAsJson': my_dictionary
    }

    return render(request, 'dashboard.html', context)
    #now = datetime.now()
    #today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    #today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    #objects = Document.objects.filter(Q(date__gte=today_min) & Q(date__lte=today_max))





@login_required
def Employees(request):
    employees = Employee.objects.all().values('first_name', 'last_name', 'username', 'email', 'date_joined')
    context = {
        'employeesAsJson': json.dumps(list(employees), default=str),
        'range': range(Employee.objects.all().__len__()),
    }
    return render(request, 'employees.html', context)


@login_required
def EmployeeDetails(request, username):
    employee = Employee.objects.get(username=username)
    context = {
        'employee': employee
    }
    return render(request, 'employee-details.html', context)


@login_required
def Documents(request):
    documents = Document.objects.all().values("title", "uploaded_at", "criticality", "file")
    context = {
        'documents': documents,
        'documentsAsJson': json.dumps(list(documents), default=str),
        'range': range(Document.objects.all().__len__()),
    }
    return render(request, 'documents.html', context)


@login_required
def DocumentDetails(request, file):
    document = Document.objects.get(file=file)
    if request.user.has_perm("view_document", document) and \
            request.user.has_perm("add_document", document) and \
            request.user.has_perm("edit_document", document) and \
            request.user.has_perm("delete_document", document):
        has_all_perms = True
    else:
        has_all_perms = False
    mailto_link = "joanna.prawosudowicz@gmail.com"
    context = {
        'mailto_link': mailto_link,
        'has_all_perms': has_all_perms,
        'user_permissions': {
            'view_document': request.user.has_perm("view_document", document),
            'add_document': request.user.has_perm("add_document", document),
            'edit_document': request.user.has_perm("edit_document", document),
            'delete_document': request.user.has_perm("delete_document", document),
        },
        'user': request.user,
        'document': document
    }
    return render(request, 'document-details.html', context)


# @login_required
# def Correspondents(request):
#     return render(request, 'password_reset_form.html')


@login_required
def Upload(request):
    # process uploaded file
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            return RequestPermissions(request, obj.id)
    else:
        form = DocumentForm()
    # load page normally
    return render(request, 'upload.html', {'form': form})


@login_required
def ViewProtectedFile(request, path):
    # Check user permissions or any other access control logic here
    if not request.user.has_perm('home.view_document'):
        return HttpResponseForbidden("You don't have permission to access this media.")

    # Construct the full path to the media file
    media_path = os.path.join(settings.MEDIA_ROOT, path)

    # Serve the file
    with open(media_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')

    return response

def delete_document(request, document_id):
    document = Document.objects.get(id=document_id)
    if request.user.has_perm('delete_document', document):
        document.delete()
    else:
        return HttpResponseForbidden("You don't have permission to delete this file.")
    return render(request, 'delete_document.html')


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

    if request.method == 'POST':
        form = ApproveOrRejectRequest(request.POST)
        if form.is_valid():
            if form.cleaned_data["choice"] == "approve":
                print("FORM APPROVED!!!1!!!")
                if permission_request.requested_permission == "view_document":
                    assign_perm(permission_request.requested_permission, requester, document)
                elif permission_request.requested_permission == "add_document":
                    pass
                elif permission_request.requested_permission == "delete_document":
                    document.delete()
                    return render(request, 'delete_document.html')
            elif form.cleaned_data["choice"] == "reject":
                if permission_request.requested_permission == "add_document":
                    document.delete()
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
                  })