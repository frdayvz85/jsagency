# Generated by Django 3.1.7 on 2021-11-06 14:55

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_job_worktype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
