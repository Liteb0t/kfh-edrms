from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shangoedrms", views.shangoedrms, name="shangoedrms"),
    path('members/', views.members, name='members'),
    path("employees/", views.Employees, name="employees"),
    path("documents/", views.Documents, name="documents"),
    path("login/", views.Login, name="login")
]

