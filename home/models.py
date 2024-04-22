import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class Employee(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Name, email, and password are included already with AbstractUser
    phone = models.CharField(max_length=16, null=True)

    # PROTECT: Employees must be reassigned before branch/role can be deleted
    branch = models.ForeignKey("Branch", on_delete=models.PROTECT, default=None, null=True)
    # "roles" are now handled as groups in Django's permission system
    # role = models.ForeignKey("Role", on_delete=models.PROTECT, default=None, null=True)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.FileField(default="yes.png")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # when Employee is deleted, uploaded_by becomes blank but Document remains
    uploaded_by = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True)
    # file_name = models.CharField(max_length=50, default="Sample_Bank_Document.pdf")
    criticality = models.CharField(max_length=50, null=False,
                                   choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')


class DocumentAccessRequest(models.Model):
    id = models.AutoField(primary_key=True)
    reason_given = models.CharField(max_length=2000, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    requested_permission = models.CharField(max_length=100, null=False, choices=[
        ('add_document', 'Upload Document'),
        ('view_document', 'View Document'),
        ('change_document', 'Change Document'),
        ('delete_document', 'Delete Document'),
    ], default='view_document')
    pending = models.BooleanField(default=True)
    document = models.ForeignKey("Document", on_delete=models.CASCADE)  # When document is deleted request is deleted
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name="requester")  # When employee is deleted request is deleted
    # supervisor = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name="supervisor")
    request_groups = models.ManyToManyField(Group, blank=True)
    request_employees = models.ManyToManyField(Employee, blank=True)
