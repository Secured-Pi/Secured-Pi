# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securedpi_events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='action',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
