# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-17 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enterprise', '0003_auto_20170520_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='code',
            field=models.IntegerField(default=204),
        ),
    ]
