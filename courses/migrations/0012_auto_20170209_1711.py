# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 17:11
from __future__ import unicode_literals

from django.db import migrations, models
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_reviewsession_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modulevideo',
            options={'verbose_name': 'video'},
        ),
        migrations.AlterModelOptions(
            name='reviewsession',
            options={'verbose_name': 'Review'},
        ),
        migrations.AlterModelOptions(
            name='studentbooking',
            options={'verbose_name': 'participation'},
        ),
        migrations.AlterModelOptions(
            name='studentprogress',
            options={'verbose_name': 'certificate'},
        ),
        migrations.AddField(
            model_name='studentbooking',
            name='confirmed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='module',
            name='outcomes',
            field=django_markdown.models.MarkdownField(),
        ),
    ]