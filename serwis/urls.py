from django.urls import path
from .views import nowy_RodzajUsterek, nowe_Urzadzenie, nowy_serwisant, nowe_zgloszenie, login_request, logout_request, wpisy


urlpatterns = [
        path('', wpisy, name='wpisy'),
        path('nowe_zgloszenie/', nowe_zgloszenie, name='nowe_zgloszenie'),
        path('nowy_rodzaj_usterki/', nowy_RodzajUsterek, name='nowy_RodzajUsterek'),
        path('nowe_urzadzenia/', nowe_Urzadzenie, name='nowe_Urzadzenie'),
        path('nowy_serwisant/', nowy_serwisant, name='nowy_serwisant'),
        path('login/', login_request, name='login'),
        path('logout/', logout_request, name='logout'),
    ]