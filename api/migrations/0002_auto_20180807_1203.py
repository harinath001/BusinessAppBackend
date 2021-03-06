# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-07 12:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='USER_USER', to='api.User'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='id',
            field=models.UUIDField(default=b'e8526c6e-4aca-4d71-9d27-a1854a2fbc41', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='id',
            field=models.UUIDField(default=b'18e7d355-2dc5-4bb0-a176-b98b9d3a3d41', editable=False, primary_key=True, serialize=False),
        ),
    ]
