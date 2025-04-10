from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("outgoing-requests/", views.OutgoingRequests, name="outgoing-requests"),
    path("incoming-requests/", views.IncomingRequests, name="incoming-requests"),
    #path("", views.Pendings, name="index"),
    path("employees/", views.Employees, name="employees"),
    # path("employees/<int:branch_id>/", views.EmployeesAtYourBranch, name="employees"),
    path("employees/<str:username>/", views.EmployeeDetails, name="employee_details"),
    # path("login/", views.Login, name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("correspondents/", views.Correspondents, name="correspondents"),
    path("upload/", views.Upload, name="upload"),
    # path("media/<str:path>", views.ViewProtectedFile, name="protected_media"),
    path("branches/", views.Branches, name="branches"),
    path("branches/<int:branch_id>/", views.BranchDetails, name="branch_details"),
    path("branches/<int:branch_id>/employees/", views.BranchEmployees, name="branch_employees"),
    path("documents/", views.Documents, name="documents"),
    path("documents/recently-uploaded/", views.RecentlyUploadedDocuments, name="recently_uploaded_documents"),
    path("documents/recently-deleted/", views.RecentlyDeletedDocuments, name="recently_deleted_documents"),
    path("documents/<int:document_id>/", views.DocumentDetails, name="document_details"),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('documents/<int:document_id>/preview/', views.PreviewDocument, name='preview_document'),
    path('documents/<int:document_id>/download/', views.DownloadDocument, name='download_document'),
    path('documents/<int:document_id>/view/', views.ViewDocument, name='view_document'),
    path('documents/<int:document_id>/request-permissions/', views.RequestPermissions, name='request_permissions'),
    path('documents/<int:document_id>/edit/', views.EditDocument, name='edit_document'),
    path('documents/<int:document_id>/history/', views.DocumentHistory, name='document_history'),
    path('review-permission-request/<int:request_id>/', views.ReviewPermissionRequest, name='review_permission_request'),
    #path('documents/<int:document_id>/accessdenied/', views.document_access, name='access_denied'),
    # Other URL patterns
]
