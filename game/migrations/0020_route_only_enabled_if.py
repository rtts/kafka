# Generated by Django 2.1.1 on 2018-11-29 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_auto_20181122_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='only_enabled_if',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='game.Route', verbose_name='Als de speler deze keuze ooit heeft gemaakt'),
        ),
    ]