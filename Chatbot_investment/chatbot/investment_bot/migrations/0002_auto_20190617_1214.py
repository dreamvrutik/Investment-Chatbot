# Generated by Django 2.2.2 on 2019-06-17 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investment_bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_database',
            name='Date_of_Join',
        ),
        migrations.RemoveField(
            model_name='user_database',
            name='dob',
        ),
    ]