# Generated by Django 3.1.7 on 2021-10-29 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_about_category_comment_contactformmessage_contactinfo_country_employee_employer_job_jobcategory_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='profile_pic',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]
