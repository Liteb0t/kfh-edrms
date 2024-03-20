# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from home.models import Employee, Document


# Dashboard
def index(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render())


def Employees(request):
    employees = Employee.objects.all().values()
    template = loader.get_template('employees.html')
    context = {
        'employees': employees,
        'range': range(Employee.objects.all().__len__()),
        'table_row_count': Employee.objects.all().__len__()
    }
    return HttpResponse(template.render(context, request))

def EmployeeDetails(request, id):
    employee = Employee.objects.get(id=id)
    template = loader.get_template('employee-details.html')
    context = {
        'employee': employee
    }
    return HttpResponse(template.render(context, request))

def Documents(request):
    documents = Document.objects.all().values()
    template = loader.get_template('documents.html')
    context = {
        'documents': documents,
    }
    return HttpResponse(template.render(context, request))

def Login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

