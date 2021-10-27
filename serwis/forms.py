from django.forms import ModelForm
from django import forms
from .models import RodzajUsterki, Urzadzenie, Serwisant, Zgloszenie


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


class SerwisantForm(ModelForm):
    class Meta:
        model = Serwisant
        fields = [
            'nr_serwisanta',
            'imie',
            'nazwisko',
            'aktywny',
        ]


class ZgloszeniForm(ModelForm):
    class Meta:
        model = Zgloszenie
        fields = [
            'data_zgloszenia',
            'temat_zgloszenia',
            'opis_zgloszenia',
            'zglaszajacy',
        ]