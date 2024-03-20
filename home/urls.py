from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("employees/", views.Employees, name="employees"),
    path("employees/details/<int:id>", views.EmployeeDetails, name="employee_details"),
    path("documents/", views.Documents, name="documents"),
    path("login/", views.Login, name="login")
]

