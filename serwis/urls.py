from django.urls import path
from .views import nowy_RodzajUsterek, nowe_Urzadzenie, nowy_serwisant


urlpatterns = [
        path('', nowy_RodzajUsterek, name='nowy_RodzajUsterek'),
        path('nowe_urzadzenia/', nowe_Urzadzenie, name='nowe_Urzadzenie'),
        path('nowy_serwisant/', nowy_serwisant, name='nowy_serwisant'),
    ]