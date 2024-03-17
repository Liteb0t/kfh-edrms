# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from home.models import Employee


# Dashboard
def index(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render())


def Employees(request):
    employees = Employee.objects.all().values()
    template = loader.get_template('employees.html')
    context = {
        'employees': employees,
    }
    return HttpResponse(template.render(context, request))

def Documents(request):
    template = loader.get_template('documents.html')
    return HttpResponse(template.render())

def Login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

