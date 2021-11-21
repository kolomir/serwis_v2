from django.urls import path
from .views import nowy_RodzajUsterek, nowe_Urzadzenie, nowy_serwisant, nowe_zgloszenie, login_request, logout_request, wpisy, wpis_szczegoly, autorzy, anuluj_zgloszenie


urlpatterns = [
        path('', wpisy, name='wpisy'),
        path('zgloszenie/<int:id>/', wpis_szczegoly, name='wpis_szczegoly'),
        path('nowe_zgloszenie/', nowe_zgloszenie, name='nowe_zgloszenie'),
        path('nowy_rodzaj_usterki/', nowy_RodzajUsterek, name='nowy_RodzajUsterek'),
        path('nowe_urzadzenia/', nowe_Urzadzenie, name='nowe_Urzadzenie'),
        path('nowy_serwisant/', nowy_serwisant, name='nowy_serwisant'),
        #- KASOWANIE -----------------------------------------------------------
        path('potwierdz_anuluj_zgloszenie/<int:id>/', anuluj_zgloszenie, name='anuluj_zgloszenie'),
        #- SYSTEM --------------------------------------------------------------
        path('login/', login_request, name='login'),
        path('logout/', logout_request, name='logout'),
        #-----------------------------------------------------------------------
        path('test/', autorzy, name='autorzy'),
    ]