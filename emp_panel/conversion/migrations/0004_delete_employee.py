# Generated by Django 5.2.1 on 2025-07-15 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversion', '0003_employee_date_employee_intime1_employee_intime2_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
