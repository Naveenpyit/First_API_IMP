# Generated by Django 5.1.5 on 2025-01-29 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mnc', '0005_new_main_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_main_table',
            name='Duration',
            field=models.CharField(default=2, max_length=3),
        ),
    ]
