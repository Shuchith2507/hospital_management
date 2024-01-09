# Generated by Django 5.0.1 on 2024-01-09 05:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalapp', '0007_remove_patient_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='age',
        ),
        migrations.AddField(
            model_name='patient',
            name='dob',
            field=models.DateField(default='2024-01-09'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='entry_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
