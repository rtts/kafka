# Generated by Django 2.1.1 on 2019-02-11 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_condition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='only_enabled_if',
        ),
    ]
