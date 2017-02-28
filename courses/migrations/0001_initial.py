# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('year', models.IntegerField(default=2017)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=60)),
                ('country', models.CharField(max_length=60)),
                ('continent', models.CharField(max_length=60)),
                ('website', models.URLField()),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Program')),
            ],
        ),
    ]
