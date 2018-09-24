# Generated by Django 2.1.1 on 2018-09-24 19:50

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kafka', '0014_emoji_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('emoji', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kafka.Emoji', verbose_name='emoji')),
            ],
            options={
                'verbose_name': 'karakter',
                'verbose_name_plural': 'karakters',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'bericht',
                'verbose_name_plural': 'berichten',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applies_to', models.ManyToManyField(related_name='_route_applies_to_+', to='game.Character', verbose_name='van toepassing op')),
            ],
            options={
                'verbose_name': 'route',
                'verbose_name_plural': 'routes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('routes', models.ManyToManyField(through='game.Route', to='game.Screen', verbose_name='routes')),
            ],
            options={
                'verbose_name': 'scherm',
                'verbose_name_plural': 'schermen',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ScreenType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveIntegerField(choices=[(10, 'Keuze'), (11, 'Willekeurige keuze'), (20, 'Actie'), (30, 'Locatie'), (40, 'Mededeling'), (50, 'Gesprek')], unique=True, verbose_name='soort')),
                ('background_image', models.ImageField(blank=True, upload_to='', verbose_name='achtergrondafbeelding')),
            ],
            options={
                'verbose_name': 'schermtype',
                'verbose_name_plural': 'schermtypes',
                'ordering': ['type'],
            },
        ),
        migrations.AddField(
            model_name='screen',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.ScreenType', verbose_name='type'),
        ),
        migrations.AddField(
            model_name='route',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.Screen', verbose_name='van'),
        ),
        migrations.AddField(
            model_name='route',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.Screen', verbose_name='naar'),
        ),
        migrations.AddField(
            model_name='message',
            name='screen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='game.Screen', verbose_name='scherm'),
        ),
        migrations.AddField(
            model_name='character',
            name='first_screen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.Screen', verbose_name='eerste scherm'),
        ),
    ]
