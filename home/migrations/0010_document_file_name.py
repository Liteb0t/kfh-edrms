# Generated by Django 5.0.3 on 2024-03-20 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_employee_last_name_alter_employee_middle_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file_name',
            field=models.CharField(default='Sample_Bank_Document.pdf', max_length=50),
        ),
    ]
