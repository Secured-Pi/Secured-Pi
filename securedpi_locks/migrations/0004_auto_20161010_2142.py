# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 21:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securedpi_locks', '0003_auto_20161010_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lock',
            old_name='date_uploaded',
            new_name='date_created',
        ),
    ]