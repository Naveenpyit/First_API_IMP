# Generated by Django 5.1.5 on 2025-01-29 06:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mnc', '0004_alter_example_master_last_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_main_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Table_Name', models.CharField(max_length=40)),
                ('Last_Update', models.DateTimeField(default=django.utils.timezone.now)),
                ('Duration', models.CharField(max_length=3)),
                ('New_Update', models.CharField(default='No', max_length=3)),
            ],
        ),
    ]
