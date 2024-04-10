from django.urls import path, include
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.Pendings, name="index"),
    path("employees/", views.Employees, name="employees"),
    path("employees/details/<int:id>", views.EmployeeDetails, name="employee_details"),
    path("documents/", views.Documents, name="documents"),
    path("documents/details/<int:id>", views.DocumentDetails, name="document_details"),
    # path("login/", views.Login, name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("correspondants", views.Correspondants, name="correspondants"),
]

