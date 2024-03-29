# Generated by Django 2.1.1 on 2019-01-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_screen_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screentype',
            name='type',
            field=models.PositiveIntegerField(choices=[(5, 'Introscherm'), (10, 'Keuze (geel)'), (11, 'Willekeurige keuze'), (20, 'Actie (groen)'), (30, 'Locatie (blauw)'), (40, 'Mededeling (rood)'), (50, 'Gesprek (oranje)'), (60, 'Video (grijs)')], unique=True, verbose_name='soort'),
        ),
    ]
