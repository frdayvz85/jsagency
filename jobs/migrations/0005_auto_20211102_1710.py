# Generated by Django 3.1.7 on 2021-11-02 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20211102_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='company_logo',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='profile_pic',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
