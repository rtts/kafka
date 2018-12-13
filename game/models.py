from django.db import models
from django.utils.safestring import mark_safe
from numberedmodel.models import NumberedModel
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from kafka.models import Emoji

class Color(models.Model):
    name = models.CharField('naam', max_length=32)
    color = ColorField('kleurcode')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'kleur'
        verbose_name_plural = 'kleuren'
        ordering = ['name']

class Character(NumberedModel):
    position = models.PositiveIntegerField('positie op het karakterkeuzescherm', blank=True)
    title = models.CharField('titel', max_length=255)
    active = models.BooleanField('actief', default=True)
    first_screen = models.ForeignKey('Screen', on_delete=models.PROTECT, verbose_name='eerste scherm')
    emoji = models.ImageField('afbeelding', blank=True, help_text='Dit is het pictogram van dit karakter op het keuzescherm')
    image = models.ImageField('afbeelding', blank=True, help_text='Dit is de afbeelding die wordt getoond nadat de speler het karakter heeft gekozen')
    color = models.CharField('kleur', max_length=16, blank=True)
    intro = RichTextField('introductietekst', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'karakter'
        verbose_name_plural = 'karakters'
        ordering = ['position']

class ScreenType(models.Model):
    TYPES = [
        (5, 'Introscherm'),
        (10, 'Keuze (geel)'),
        (11, 'Willekeurige keuze'),
        (20, 'Actie (groen)'),
        (30, 'Locatie (blauw)'),
        (40, 'Mededeling (rood)'),
        (50, 'Gesprek (oranje)'),
    ]
    type = models.PositiveIntegerField('soort', choices=TYPES, unique=True)
    color = models.CharField('kleurcode (in de graaf)', max_length=16, blank=True)
    foreground_color = models.ForeignKey(Color, verbose_name='voorgrondkleur', blank=True, null=True, on_delete=models.PROTECT, related_name='+')
    background_color = models.ForeignKey(Color, verbose_name='achtergrondkleur', blank=True, null=True, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return self.get_type_display()

    class Meta:
        verbose_name = 'schermtype'
        verbose_name_plural = 'schermtypes'
        ordering = ['type']

class Screen(models.Model):
    title = models.CharField('titel', max_length=255)
    type = models.ForeignKey(ScreenType, on_delete=models.CASCADE, related_name='+', verbose_name='type')
    image = models.ImageField('afbeelding', blank=True)
    button_text = models.CharField('tekst op de "Verder"-knop', max_length=255, blank=True)
    foreground_color = models.ForeignKey(Color, verbose_name='voorgrondkleur', blank=True, null=True, on_delete=models.PROTECT, related_name='+')
    background_color = models.ForeignKey(Color, verbose_name='achtergrondkleur', blank=True, null=True, on_delete=models.PROTECT, related_name='+')
    text_color = models.ForeignKey(Color, verbose_name='tekstkleur', blank=True, null=True, on_delete=models.PROTECT, related_name='+')
    button_color = models.ForeignKey(Color, verbose_name='buttonkleur', help_text='wordt nu niet gebruikt', blank=True, null=True, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return '{}. {}'.format(self.id, self.title)

    class Meta:
        verbose_name = 'scherm'
        verbose_name_plural = 'schermen'
        ordering = ['id']

class Route(models.Model):
    name = models.CharField('naam', max_length=255, blank=True)
    source = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='routes', verbose_name='van')
    target = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='+', verbose_name='naar')
    applies_to = models.ManyToManyField(Character, blank=True, related_name='+', verbose_name='van toepassing op')
    only_enabled_if = models.ForeignKey('self', on_delete=models.PROTECT, related_name='+', verbose_name='Als de speler deze keuze ooit heeft gemaakt', blank=True, null=True)
    disabled = models.BooleanField('niet mogelijk om aan te klikken', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'route'
        verbose_name_plural = 'routes'
        ordering = ['id']

class Message(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True, null=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='messages', verbose_name='scherm')
    received = models.BooleanField('ontvangen bericht', default=False)
    content = RichTextField(blank=True)

    def __str__(self):
        return mark_safe(self.content)

    def number_with_respect_to(self):
        return self.screen.messages.all()

    class Meta:
        verbose_name = 'bericht'
        verbose_name_plural = 'berichten'
        ordering = ['position']

# Todo: twee identieke subbomen (op een scherm na) op basis van wel/niet brp keuze
