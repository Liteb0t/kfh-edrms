# Generated by Django 3.2.25 on 2024-04-22 17:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20240422_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='manually_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='document',
            name='delete_at',
            field=models.DateTimeField(default=datetime.datetime(2031, 4, 21, 17, 39, 45, 981882, tzinfo=utc)),
        ),
    ]
