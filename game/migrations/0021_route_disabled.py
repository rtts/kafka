# Generated by Django 2.1.1 on 2018-11-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_route_only_enabled_if'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='disabled',
            field=models.BooleanField(default=False, verbose_name='niet mogelijk om aan te klikken'),
        ),
    ]