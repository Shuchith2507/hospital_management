# Generated by Django 5.0.1 on 2024-01-09 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalapp', '0006_patient_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='created_at',
        ),
    ]