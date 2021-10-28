from django.contrib import admin
from .models import Autor, RodzajUsterki, Urzadzenie, Serwisant, Status, Zgloszenie


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_filter = ('aktywny',)


@admin.register(RodzajUsterki)
class RodzajUsterkiAdmin(admin.ModelAdmin):
    list_display = ('id', 'rodzaj_usterki', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('rodzaj_usterki', 'aktywny')


@admin.register(Urzadzenie)
class UrzadzenieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nazwa_urzadzenia', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('nazwa_urzadzenia', 'aktywny')


@admin.register(Serwisant)
class SerwisantAdmin(admin.ModelAdmin):
    list_display = ('id', 'nr_serwisanta', 'imie', 'nazwisko', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('nr_serwisanta', 'imie', 'nazwisko', 'aktywny')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'nazwa', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('nazwa', 'aktywny')


@admin.register(Zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ('id', 'temat_zgloszenia', 'data_zgloszenia', 'zglaszajacy', 'rodzaj_usterki', 'urzadzenie', 'status')
    list_filter = ('zglaszajacy', 'rodzaj_usterki', 'urzadzenie', 'status')
    search_fields = ('id', 'temat_zgloszenia', 'data_zgloszenia', 'zglaszajacy', 'rodzaj_usterki', 'urzadzenie', 'status')