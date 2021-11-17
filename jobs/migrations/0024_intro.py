# Generated by Django 3.1.7 on 2021-11-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0023_auto_20211117_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('overview', models.TextField(blank=True, max_length=700, null=True, verbose_name='Overview')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Description')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Applied time')),
            ],
            options={
                'verbose_name': 'Intro',
                'verbose_name_plural': 'Intro',
            },
        ),
    ]
