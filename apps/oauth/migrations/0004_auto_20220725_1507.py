# Generated by Django 3.2.5 on 2022-07-25 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0003_auto_20220522_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birth_year',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city_state',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ethnicity',
        ),
        migrations.RemoveField(
            model_name='user',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
