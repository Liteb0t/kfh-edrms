from django.shortcuts import render
# from django.core import serializers
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.template import loader
from django.contrib.auth.decorators import login_required

from home.forms import DocumentForm
from home.models import Employee, Document, Pending
import json


@login_required
def index(request):
    # we still pass 'request' which contains the logged-in user
    # without it, the "logged in as [...]" would not work
    return render(request, 'dashboard.html')

@login_required
def Employees(request):
    employees = Employee.objects.all().values('email', 'first_name', 'last_name', 'phone')
    context = {
        'employeesAsJson': json.dumps(list(employees), default=str),
        'range': range(Employee.objects.all().__len__()),
    }
    return render(request,'employees.html', context)

@login_required
def EmployeeDetails(request, id):
    employee = Employee.objects.get(id=id)
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


@login_required
def Correspondents(request):
    return render(request, 'correspondents.html')


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