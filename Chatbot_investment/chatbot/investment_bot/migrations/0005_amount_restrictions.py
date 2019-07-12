# Generated by Django 2.2.1 on 2019-06-26 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment_bot', '0004_section_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount_Restrictions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.CharField(max_length=100)),
                ('subsection_id', models.CharField(max_length=100)),
                ('Max_Amount', models.IntegerField()),
                ('Additional_Amount', models.IntegerField()),
            ],
            options={
                'unique_together': {('section_id', 'subsection_id')},
            },
        ),
    ]