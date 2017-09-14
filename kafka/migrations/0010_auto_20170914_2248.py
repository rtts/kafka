# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 20:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kafka', '0009_webtext'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worksession',
            options={'ordering': ['position'], 'verbose_name': 'Werksessie'},
        ),
        migrations.AddField(
            model_name='worksession',
            name='position',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='positie'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='webtext',
            name='parameter',
            field=models.PositiveIntegerField(choices=[(1, 'Homepage tekst'), (100, 'Footer tekst')]),
        ),
        migrations.AlterField(
            model_name='worksession',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='kafka.Event', verbose_name='evenement'),
        ),
    ]
