# Generated by Django 5.1.5 on 2025-01-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mnc', '0002_example_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example_master',
            name='Last_Update',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
