# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-07 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('middleware', '0002_auto_20180807_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='id',
            field=models.UUIDField(default=b'399fb0ed-cf87-423b-99ed-22a86d0b3bdf', editable=False, primary_key=True, serialize=False),
        ),
    ]