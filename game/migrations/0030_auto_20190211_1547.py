# Generated by Django 2.1.1 on 2019-02-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_remove_screen_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='audio',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='screen',
            name='video',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
