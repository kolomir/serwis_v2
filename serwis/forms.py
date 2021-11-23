from django.forms import ModelForm
from django import forms
from .models import RodzajUsterki, Urzadzenie, Serwisant, Status, Zgloszenie, Comments


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = [
            'zgloszenie',
            'tresc'
        ]

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


class WykonanieZgloszenie(ModelForm):
    class Meta:
        model = Zgloszenie
        fields = [
            'status',
            'data_wykonania',
            'czas_wykonania',
        ]


class AnulowacZgloszenie(ModelForm):
    class Meta:
        model = Zgloszenie
        fields = [
            'status',
            'data_zamkniecia',
            'czas_zamkniecia',
        ]


class ZawieszenieZgloszenia(ModelForm):
    class Meta:
        model = Zgloszenie
        fields = [
            'status',
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