# Generated by Django 3.1.7 on 2021-11-03 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_auto_20211103_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='featured',
        ),
    ]