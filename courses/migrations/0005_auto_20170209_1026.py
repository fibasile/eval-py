# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 10:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_module_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('kind', models.CharField(choices=[('review', 'Review'), ('lecture', 'Lecture'), ('misc', 'Misc')], default='review', max_length=8)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='module',
            name='webpage',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='modulevideo',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Module'),
        ),
    ]
