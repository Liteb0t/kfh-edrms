# Generated by Django 5.0.3 on 2024-03-17 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_branch_employee_password_employee_branch_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.branch'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]