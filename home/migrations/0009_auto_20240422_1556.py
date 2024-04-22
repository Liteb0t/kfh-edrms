# Generated by Django 3.2.25 on 2024-04-22 15:56

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('home', '0008_alter_documentaccessrequest_requested_permission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='role',
        ),
        migrations.AddField(
            model_name='document',
            name='delete_at',
            field=models.DateTimeField(default=datetime.datetime(2031, 4, 21, 15, 56, 31, 523612, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='documentaccessrequest',
            name='request_employees',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documentaccessrequest',
            name='request_groups',
            field=models.ManyToManyField(blank=True, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='documentaccessrequest',
            name='requested_permission',
            field=models.CharField(choices=[('add_document', 'Upload Document'), ('view_document', 'View Document'), ('change_document', 'Edit Document'), ('delete_document', 'Delete Document')], default='view_document', max_length=100),
        ),
    ]
