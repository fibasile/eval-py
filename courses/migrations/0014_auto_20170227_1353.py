# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20170209_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(default='', max_length=60),
        ),
    ]
