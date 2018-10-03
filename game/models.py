from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from kafka.models import Emoji

class Character(models.Model):
    title = models.CharField('titel', max_length=255)
    first_screen = models.ForeignKey('Screen', on_delete=models.PROTECT, verbose_name='eerste scherm')
    emoji = models.ForeignKey(Emoji, on_delete=models.PROTECT, verbose_name='emoji')
    color = models.CharField('kleur', max_length=16, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'karakter'
        verbose_name_plural = 'karakters'
        ordering = ['title']

class ScreenType(models.Model):
    TYPES = [
        (10, 'Keuze (geel)'),
        (11, 'Willekeurige keuze'),
        (20, 'Actie (groen)'),
        (30, 'Locatie (blauw)'),
        (40, 'Mededeling (rood)'),
        (50, 'Gesprek (oranje)'),
    ]
    type = models.PositiveIntegerField('soort', choices=TYPES, unique=True)
    color = models.CharField('kleur', max_length=16, blank=True)
    background_image = models.ImageField('achtergrondafbeelding', blank=True)

    def __str__(self):
        return self.get_type_display()

    class Meta:
        verbose_name = 'schermtype'
        verbose_name_plural = 'schermtypes'
        ordering = ['type']

class Location(models.Model):
    title = models.CharField('titel', max_length=255)
    background_image = models.ImageField('achtergrondafbeelding', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'locatie'
        verbose_name_plural = 'locaties'
        ordering = ['title']

class Screen(models.Model):
    title = models.CharField('titel', max_length=255)
    type = models.ForeignKey(ScreenType, on_delete=models.CASCADE, related_name='+', verbose_name='type', blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+', verbose_name='locatie', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'scherm'
        verbose_name_plural = 'schermen'
        ordering = ['title']

class Route(models.Model):
    name = models.CharField('naam', max_length=255, blank=True)
    source = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='routes', verbose_name='van')
    target = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='+', verbose_name='naar')
    applies_to = models.ManyToManyField(Character, blank=True, related_name='+', verbose_name='van toepassing op')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'route'
        verbose_name_plural = 'routes'
        ordering = ['id']

class Message(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='messages', verbose_name='scherm')
    content = RichTextField(blank=True)

    def __str__(self):
        return mark_safe(self.content)

    class Meta:
        verbose_name = 'bericht'
        verbose_name_plural = 'berichten'
        ordering = ['id']

# Todo: twee identieke subbomen (op een scherm na) op basis van wel/niet brp keuze
