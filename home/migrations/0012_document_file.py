# Generated by Django 5.0.3 on 2024-04-11 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(default='documents/default.pdf', upload_to='documents/'),
        ),
    ]
