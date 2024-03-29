# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kafka', '0011_auto_20170914_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='page',
        ),
        migrations.AlterField(
            model_name='documentation',
            name='slug',
            field=models.SlugField(help_text='Deze tekst wordt gebruik in de URL naar deze documentatie', unique=True),
        ),
        migrations.AlterField(
            model_name='worksession',
            name='slug',
            field=models.SlugField(help_text='Deze tekst wordt gebruik in de URL naar deze documentatie', null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
    ]
