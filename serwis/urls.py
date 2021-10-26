from django.urls import path
from .views import nowy_RodzajUsterek, nowe_Urzadzenie


urlpatterns = [
        path('', nowy_RodzajUsterek, name='nowy_RodzajUsterek'),
        path('nowe_urzadzenia/', nowe_Urzadzenie, name='nowe_Urzadzenie'),
    ]