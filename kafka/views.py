from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import *
from .utils import *

class Homepage(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'content': get_webtext(1),
            'footer': get_webtext(100),
            'event': Event.objects.first(),
        })
        return context

class Session(DetailView):
    model = WorkSession
    template_name = 'session.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'footer': get_webtext(100),
            'session': self.object,
        })
        return context
