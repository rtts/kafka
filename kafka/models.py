from django.db import models
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
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
    #image = models.ImageField('afbeelding', blank=True)
    #video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    #button = models.CharField('button', max_length=255, blank=True)
    #hyperlink = models.CharField(max_length=255, blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return 'Sectie: #{} {}'.format(self.position, self.title)

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']

class Config(models.Model):
    TYPES = [
#        (1, 'Footer tekst'),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES)
    content = models.TextField('inhoud')

    class Meta:
        verbose_name = 'Parameter'
        ordering = ['parameter']
