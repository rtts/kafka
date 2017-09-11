from django.contrib import admin

from .models import *

admin.site.site_title = 'Camping Kafka Beheer'
admin.site.site_header = 'Camping Kafka Beheer'
admin.site.index_title = 'Overzicht'

class InlineSectionAdmin(admin.StackedInline):
    model = Section
    extra = 0

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [InlineSectionAdmin]

#@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'content']
    exclude = ['parameter']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
