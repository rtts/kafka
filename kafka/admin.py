from django.contrib import admin

from .models import *

admin.site.site_title = 'Camping Kafka Beheer'
admin.site.site_header = 'Camping Kafka Beheer'
admin.site.index_title = 'Overzicht'

@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ['event']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Webtext)
class WebtextAdmin(admin.ModelAdmin):
    exclude = ['parameter']
    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

class InlineDocumentationImageAdmin(admin.StackedInline):
    model = DocumentationImage
    extra = 0

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [InlineDocumentationImageAdmin]

#@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'content']
    exclude = ['parameter']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
