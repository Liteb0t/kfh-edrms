from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("", views.Pendings, name="index"),
    path("employees/", views.Employees, name="employees"),
    path("employees/details/<str:username>", views.EmployeeDetails, name="employee_details"),
    path("documents/", views.Documents, name="documents"),
    path("documents/details/<str:file>", views.DocumentDetails, name="document_details"),
    # path("login/", views.Login, name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("correspondents/", views.Correspondents, name="correspondents"),
    path("upload/", views.Upload, name="upload"),
]
