from django.shortcuts import render
# from django.core import serializers
# from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User

from home.forms import DocumentForm
from home.models import Employee, Document, Pending
import json
from django.utils import timezone
import datetime

import os


@login_required
def index(request):
    documents = Document.objects.all().values()
    # Filter records where the datetime field falls within a specific range
    start_date = timezone.now() - timezone.timedelta(days=1)
    end_date = timezone.now()
    queryset = Document.objects.filter(uploaded_at__range=(start_date, end_date))

    context = {
        'documents': queryset,
        'documentsAsJson': json.dumps(list(documents), default=str),
        'range': range(Document.objects.all().__len__()),
    }
    return render(request, 'dashboard.html', context)
    #now = datetime.now()
    #today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    #today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    #objects = Document.objects.filter(Q(date__gte=today_min) & Q(date__lte=today_max))




@login_required
def Employees(request):
    employees = Employee.objects.all().values('first_name', 'last_name', 'username', 'date_joined')
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
def Pendings(request):
    pendings = Pending.objects.all().values()
    context = {
        'pendings': pendings,
        'pendingsAsJson': json.dumps(list(pendings), default=str),
        'range': range(Pending.objects.all().__len__()),
    }
    return render(request, 'dashboard.html', context)


@login_required
def Documents(request):
    documents = Document.objects.all().values()
    context = {
        'documents': documents,
        'documentsAsJson': json.dumps(list(documents), default=str),
        'range': range(Document.objects.all().__len__()),
    }
    return render(request, 'documents.html', context)


@login_required
def DocumentDetails(request, file):
    document = Document.objects.get(file=file)
    context = {
        'document': document
    }
    return render(request, 'document-details.html', context)


# @login_required
# def Correspondents(request):
#     return render(request, 'correspondents.html')


@login_required
def Upload(request):
    # process uploaded file
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
