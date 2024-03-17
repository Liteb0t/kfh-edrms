import uuid

from django.db import models

# Create your models here.
class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50, null=True)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)

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
    uploaded_by = models.ForeignKey("Employee", on_delete=models.CASCADE)