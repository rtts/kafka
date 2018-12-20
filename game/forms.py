from django import forms
from django.forms.widgets import RadioSelect
from .models import *

class ChooseRouteForm(forms.Form):
    route = forms.ModelChoiceField(queryset=None, widget=RadioSelect, empty_label=None, required=False)

    def __init__(self, routes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route'].queryset = routes
        if routes.exists():
            self.fields['route'].initial = routes.first().id

class ChooseScreenForm(forms.Form):
    screen_nr = forms.IntegerField(label='naar scherm nummer', required=False)
