# Generated by Django 5.2.1 on 2025-07-18 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversion', '0006_alter_conversioninfo_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='conversioninfo',
        ),
    ]
