# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-25 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0005_auto_20170624_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='number',
            field=models.IntegerField(default=870),
        ),
    ]