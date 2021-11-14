from django.forms import ModelForm
from django import forms
from .models import RodzajUsterki, Urzadzenie, Serwisant, Status, Zgloszenie


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
            'temat_zgloszenia',
            'opis_zgloszenia',
            'rodzaj_usterki',
            'urzadzenie',
        ]


class PodjecieZgloszeniaForm(ModelForm):
    class Meta:
        model = Zgloszenie
        fields = [
            'data_otwarcia',
            'czas_otwarcia',
            'serwisant',
        ]


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = [
            'nazwa',
            'aktywny'
        ]