# Generated by Django 2.1.1 on 2019-01-09 20:45

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0023_auto_20181220_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, help_text='Plak hier een Vimeo of Youtube URL', verbose_name='video'),
        ),
    ]
