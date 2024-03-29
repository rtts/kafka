# Generated by Django 2.1.1 on 2018-11-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_auto_20181122_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['position'], 'verbose_name': 'karakter', 'verbose_name_plural': 'karakters'},
        ),
        migrations.AddField(
            model_name='character',
            name='position',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='positie op het karakterkeuzescherm'),
            preserve_default=False,
        ),
    ]
