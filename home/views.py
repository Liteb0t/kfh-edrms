# from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from home.models import Employee, Document
from home.models import Pending



@login_required
def index(request):
    template = loader.get_template('dashboard.html')

    # we still pass 'request' which contains the logged-in user
    # without it, the "logged in as [...]" would not work
    return HttpResponse(template.render({}, request))

@login_required
def Employees(request):
    # if request.user.is_authenticated:
    employees = Employee.objects.all().values()
    template = loader.get_template('employees.html')
    context = {
        'employees': employees,
        'employeesAsJson': serializers.serialize('json', Employee.objects.all()),
        'range': range(Employee.objects.all().__len__()),
    }
    return HttpResponse(template.render(context, request))
    # else:
    #     return HttpResponse("Permission denied.", status=403)

@login_required
def EmployeeDetails(request, id):
    employee = Employee.objects.get(id=id)
    template = loader.get_template('employee-details.html')
    context = {
        'employee': employee
    }
    return HttpResponse(template.render(context, request))

def Pendings(request):
    pendings = Pending.objects.all().values()
    template = loader.get_template('dashboard.html')
    context = {
        'pendings': pendings,
        'range': range(Pending.objects.all().__len__()),
    }
    return HttpResponse(template.render(context,request))

@login_required
def Documents(request):
    documents = Document.objects.all().values()
    template = loader.get_template('documents.html')
    context = {
        'documents': documents,
        'range': range(Document.objects.all().__len__()),
    }
    return HttpResponse(template.render(context, request))


@login_required
def DocumentDetails(request, id):
    document = Document.objects.get(id=id)
    template = loader.get_template('document-details.html')
    context = {
        'document': document
    }
    return HttpResponse(template.render(context, request))


# def Login(request):
#     template = loader.get_template('login.html')
#     return HttpResponse(template.render())

def Profile(request):
    employee = Employee.objects.get()
    context ={
        'employee': employee
    }
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context,request))

@login_required
def Correspondants(request):
    template = loader.get_template('correspondants.html')

    # we still pass 'request' which contains the logged-in user
    # without it, the "logged in as [...]" would not work
    return HttpResponse(template.render({}, request))