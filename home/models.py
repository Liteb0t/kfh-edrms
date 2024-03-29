import uuid
from django.db import models


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=16, null=True)
    # PROTECT: Employees must be reassigned before branch/role can be deleted
    branch = models.ForeignKey("Branch", on_delete=models.PROTECT)
    role = models.ForeignKey("Role", on_delete=models.PROTECT)


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
    security_level = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # when Employee is deleted, uploaded_by becomes blank but Document remains
    uploaded_by = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True)
    file_name = models.CharField(max_length=50, default="Sample_Bank_Document.pdf")

class DocumentAccessRequest(models.Model):
    id = models.AutoField(primary_key=True)
    reason_given = models.CharField(max_length=500, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey("Document", on_delete=models.CASCADE)  # When document is deleted request is deleted
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)  # When employee is deleted request is deleted
    supervisor = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name="supervisor")
