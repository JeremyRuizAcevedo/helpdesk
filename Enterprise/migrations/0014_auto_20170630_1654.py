# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enterprise', '0013_auto_20170625_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='n_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='n_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='code',
            field=models.IntegerField(default=13201548),
        ),
    ]
