from django.shortcuts import redirect
from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple
from .models import *

class FunkySaveMixin(object):
    def response_add(self, request, obj, post_url_continue=None):
        if '_save' in request.POST:
            return redirect('graph')
        else:
            return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_save' in request.POST:
            return redirect('graph')
        else:
            return super().response_change(request, obj)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass

@admin.register(ScreenType)
class ScreenTypeAdmin(admin.ModelAdmin):
    pass

class InlineRouteAdmin(admin.StackedInline):
    model = Route
    extra = 0
    fk_name = 'source'
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "only_enabled_if":
            kwargs["queryset"] = Route.objects.exclude(name='')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class InlineMessageAdmin(admin.StackedInline):
    model = Message
    extra = 0

@admin.register(Screen)
class ScreenAdmin(FunkySaveMixin, admin.ModelAdmin):
    save_on_top = True
    inlines = [InlineMessageAdmin, InlineRouteAdmin]
    list_filter = ['type']
