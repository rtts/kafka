# Generated by Django 2.1.1 on 2018-09-24 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20180924_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.ScreenType', verbose_name='type'),
        ),
    ]
