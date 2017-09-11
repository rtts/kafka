from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import *

class Homepage(TemplateView):
    template_name = "page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homepage = get_object_or_404(Page, slug='')
        context['sections'] = homepage.sections.all()
        return context
