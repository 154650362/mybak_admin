# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-03 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Backup_mysql',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(blank=True, max_length=30)),
                ('task_id', models.CharField(blank=True, max_length=50)),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
                ('result', models.TextField(blank=True)),
                ('task_status', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]
