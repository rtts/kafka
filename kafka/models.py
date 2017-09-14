from django.db import models
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from numberedmodel.models import NumberedModel

class Page(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField('URL', help_text='Laat dit veld leeg voor de homepage', blank=True, unique=True)
    menu = models.BooleanField('zichtbaar in het menu', default=True)

    def __str__(self):
        return '{}. {}'.format(self.position, self.title)

    def get_absolute_url(self):
        if self.slug:
            return reverse('page', args=[self.slug])
        else:
            return '/'

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Pagina’s'
        ordering = ['position']

class Section(NumberedModel):
    types = [
        ('normal', 'Normale sectie'),
        ('program', 'Programmasectie'),
        ('footer', 'Footer'),
    ]
    page = models.ForeignKey(Page, verbose_name='pagina', related_name='sections')
    position = models.PositiveIntegerField('positie', blank=True)
    type = models.CharField('soort sectie', max_length=32, default=1, choices=types)
    title = models.CharField('titel', max_length=255, blank=True)
    contents = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    #button = models.CharField('button', max_length=255, blank=True)
    #hyperlink = models.CharField(max_length=255, blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return 'Sectie: #{} {}'.format(self.position, self.title)

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']

class Webtext(models.Model):
    TYPES = [
        (1, 'Homepage tekst'),
        (100, 'Footer tekst'),
    ]
    parameter = models.PositiveIntegerField(choices=TYPES)
    content = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    #button = models.CharField('button', max_length=255, blank=True)
    #hyperlink = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.get_parameter_display()

    class Meta:
        verbose_name = 'Webtekst'
        verbose_name_plural = 'Webteksten'
        ordering = ['parameter']

class WorkSession(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField(help_text='Deze text wordt gebruik in de URL naar deze documentatie', null=True, unique=True)
    event = models.ForeignKey('Event', verbose_name='evenement', related_name='sessions', blank=True, null=True)
    date = models.DateField('datum', blank=True, null=True)
    begin_time = models.TimeField('begintijd', blank=True, null=True)
    end_time = models.TimeField('eindtijd', blank=True, null=True)
    description = RichTextField('beschrijving', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
        verbose_name = 'Werksessie'

class Documentation(models.Model):
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField(help_text='Deze text wordt gebruik in de URL naar deze documentatie', unique=True)
    worksession = models.ForeignKey('WorkSession', related_name='documentations', verbose_name='werksessie', help_text='Kies hier een optionele werksessie waar deze documentatie bij hoort', blank=True, null=True)
    content = RichTextField('inhoud', blank=True)
    video = EmbedVideoField(help_text="Plak hier een YouTube of Vimeo link", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Documentatie'
        verbose_name_plural = 'Documentaties'

class DocumentationImage(models.Model):
    caption = models.CharField('bijschrift', max_length=255)
    image = models.ImageField()
    doc = models.ForeignKey('Documentation')

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['caption']
        verbose_name = 'Foto'
        verbose_name_plural = 'Foto’s'

class News(models.Model):
    date = models.DateField('datum')
    contents = RichTextField('inhoud', blank=True)
    link = models.URLField('bron', help_text='Plak hier een optionele hyperlink naar het originele bericht', blank=True)

    def __str__(self):
        return 'Nieuwsbericht van {}'.format(self.date)

    class Meta:
        verbose_name = 'Nieuwsbericht'
        verbose_name_plural = 'Nieuwsberichten'

class Event(models.Model):
    date = models.DateField('datum')
    title = models.CharField('titel', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Evenement'
        verbose_name_plural = 'Evenementen'

class Config(models.Model):
    TYPES = [

    ]

    parameter = models.PositiveIntegerField(choices=TYPES)
    content = models.TextField('inhoud')

    class Meta:
        verbose_name = 'Configuratieparameter'
        ordering = ['parameter']
