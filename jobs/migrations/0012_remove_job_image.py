# Generated by Django 3.1.7 on 2021-11-06 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_testimonial_profession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='image',
        ),
    ]