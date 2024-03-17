from django.db import models

# Create your models here.
class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
