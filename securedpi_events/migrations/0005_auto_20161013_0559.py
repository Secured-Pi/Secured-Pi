# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 05:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securedpi_events', '0004_auto_20161013_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='action',
            field=models.CharField(default='unlock', max_length=30),
        ),
    ]
