# Generated by Django 2.2 on 2019-04-02 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_auto_20190308_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='video_desktop',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
