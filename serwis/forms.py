from django.forms import ModelForm
from django import forms
from .models import RodzajUsterki, Urzadzenie


class RodzajUsterkiForm(ModelForm):
    class Meta:
        model = RodzajUsterki
        fields = [
            'rodzaj_usterki',
            'aktywny'
        ]


class UrzadzenieForm(ModelForm):
    class Meta:
        model = Urzadzenie
        fields = [
            'nazwa_urzadzenia',
            'aktywny'
        ]