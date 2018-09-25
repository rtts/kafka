from django import forms
from django.forms.widgets import RadioSelect
from .models import *

class ChooseCharacterForm(forms.Form):
    character = forms.ModelChoiceField(queryset=Character.objects.all(), label='Karakter', widget=RadioSelect, empty_label=None)

class ChooseRouteForm(forms.Form):
    route = forms.ModelChoiceField(queryset=None, widget=RadioSelect, empty_label=None, required=False)

    def __init__(self, routes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route'].queryset = routes
        if routes.exists():
            self.fields['route'].initial = routes.first().id
