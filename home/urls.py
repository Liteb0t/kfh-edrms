from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("", views.Pendings, name="index"),
    path("employees/", views.Employees, name="employees"),
    path("employees/<str:username>/", views.EmployeeDetails, name="employee_details"),
    # path("login/", views.Login, name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("correspondents/", views.Correspondents, name="correspondents"),
    path("upload/", views.Upload, name="upload"),
    # path("media/<str:path>", views.ViewProtectedFile, name="protected_media"),
    path("documents/", views.Documents, name="documents"),
    path("documents/<int:document_id>/", views.DocumentDetails, name="document_details"),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('documents/<int:document_id>/view/', views.ViewDocument, name='view_document'),
    path('documents/<int:document_id>/request-permissions/', views.RequestPermissions, name='request_permissions'),
    path('documents/<int:document_id>/edit/', views.EditDocument, name='edit_document'),
    path('review-permission-request/<int:request_id>/', views.ReviewPermissionRequest, name='review_permission_request'),
    #path('documents/<int:document_id>/accessdenied/', views.document_access, name='access_denied'),
    # Other URL patterns
]
