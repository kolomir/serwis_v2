from django.contrib import admin
from .models import Autor, RodzajUsterki, Urzadzenie, Serwisant, Zgloszenie


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('aktywny',)


@admin.register(RodzajUsterki)
class RodzajUsterkiAdmin(admin.ModelAdmin):
    list_display = ('rodzaj_usterki', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('rodzaj_usterki', 'aktywny')


@admin.register(Urzadzenie)
class UrzadzenieAdmin(admin.ModelAdmin):
    list_display = ('nazwa_urzadzenia', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('nazwa_urzadzenia', 'aktywny')


@admin.register(Serwisant)
class SerwisantAdmin(admin.ModelAdmin):
    list_display = ('nr_serwisanta', 'imie', 'nazwisko', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('nr_serwisanta', 'imie', 'nazwisko', 'aktywny')