from django.urls import path
from .views import nowy_RodzajUsterek, edytuj_RodzajUsterek, usun_RodzajUsterek, przywroc_RodzajUsterek, nowe_Urzadzenie, edytuj_Urzadzenie, usun_Urzadzenie, przywroc_Urzadzenie, nowy_serwisant, nowe_zgloszenie, login_request, logout_request, wpisy, wpis_szczegoly, autorzy, anuluj_zgloszenie, zakoncz_zgloszenie, wpis_zamkniete, wpis_zamkniete_szczegoly


urlpatterns = [
        path('', wpisy, name='wpisy'),
        path('zgloszenie/<int:id>/', wpis_szczegoly, name='wpis_szczegoly'),
        path('nowe_zgloszenie/', nowe_zgloszenie, name='nowe_zgloszenie'),
        path('nowy_rodzaj_usterki/', nowy_RodzajUsterek, name='nowy_RodzajUsterek'),
        path('nowe_urzadzenia/', nowe_Urzadzenie, name='nowe_Urzadzenie'),
        path('nowy_serwisant/', nowy_serwisant, name='nowy_serwisant'),
        path('zamkniete/', wpis_zamkniete, name='wpis_zamkniete'),
        path('zgloszenie_hist/<int:id>/', wpis_zamkniete_szczegoly, name='wpis_zamkniete_szczegoly'),
        #- EDYTOWANIE ----------------------------------------------------------
        path('edytuj_rodzaj_usterki/<int:id>/', edytuj_RodzajUsterek, name='edytuj_RodzajUsterek'),
        path('edytuj_Urzadzenia/<int:id>/', edytuj_Urzadzenie, name='edytuj_Urzadzenie'),
        #- KASOWANIE -----------------------------------------------------------
        path('potwierdz_anuluj_zgloszenie/<int:id>/', anuluj_zgloszenie, name='anuluj_zgloszenie'),
        path('usun_RodzajUsterek/<int:id>/', usun_RodzajUsterek, name='usun_RodzajUsterek'),
        path('usun_Urzadzenie/<int:id>/', usun_Urzadzenie, name='usun_Urzadzenie'),
        #- PRZYWRACANIE --------------------------------------------------------
        path('przywroc_RodzajUsterek/<int:id>/', przywroc_RodzajUsterek, name='przywroc_RodzajUsterek'),
        path('przywroc_Urzadzenie/<int:id>/', przywroc_Urzadzenie, name='przywroc_Urzadzenie'),
        #- ZAKONCZENIE ---------------------------------------------------------
        path('potwierdz_zakoncz_zgloszenie/<int:id>/', zakoncz_zgloszenie, name='zakoncz_zgloszenie'),
        #- SYSTEM --------------------------------------------------------------
        path('login/', login_request, name='login'),
        path('logout/', logout_request, name='logout'),
        #-----------------------------------------------------------------------
        path('test/', autorzy, name='autorzy'),
    ]