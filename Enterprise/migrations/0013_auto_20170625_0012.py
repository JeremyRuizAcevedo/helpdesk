# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-25 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enterprise', '0012_auto_20170624_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='code',
            field=models.IntegerField(default=13200516),
        ),
    ]
