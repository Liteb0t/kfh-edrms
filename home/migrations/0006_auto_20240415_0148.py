# Generated by Django 3.2.25 on 2024-04-15 01:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('home', '0005_auto_20240415_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentaccessrequest',
            name='request_employees',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documentaccessrequest',
            name='request_groups',
            field=models.ManyToManyField(null=True, to='auth.Group'),
        ),
    ]
