# Generated by Django 2.1.1 on 2019-03-08 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0033_auto_20190211_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='inverse',
            field=models.BooleanField(default=False, verbose_name='Als de speler de bovenstaande keuze juist NIET heeft gemaakt'),
        ),
        migrations.AddField(
            model_name='condition',
            name='inverse2',
            field=models.BooleanField(default=False, verbose_name='Als de speler de bovenstaande keuze juist NIET heeft gemaakt'),
        ),
        migrations.AddField(
            model_name='condition',
            name='only_enabled_if2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.Route', verbose_name='OF als de speler ooit deze keuze heeft gemaakt'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='only_enabled_if',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.Route', verbose_name='Als de speler ooit deze keuze heeft gemaakt'),
        ),
    ]