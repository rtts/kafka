# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kafka', '0013_auto_20170918_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='emoji',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='zichtbaar op de homepage'),
        ),
    ]
