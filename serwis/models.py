from django.db import models
from django.contrib.auth.models import User


class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    serwis = models.BooleanField(default=False)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class RodzajUsterki(models.Model):
    rodzaj_usterki = models.CharField(max_length=60, unique=False)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.rodzaj_usterki


class Urzadzenie(models.Model):
    nazwa_urzadzenia = models.CharField(max_length=80, unique=False)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa_urzadzenia


class Serwisant(models.Model):
    nr_serwisanta = models.DecimalField(max_digits=4, decimal_places=0, unique=True)
    imie = models.CharField(max_length=80, unique=False)
    nazwisko = models.CharField(max_length=80, unique=False)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return str(self.nr_serwisanta)

class Status(models.Model):
    nazwa = models.CharField(max_length=40, unique=True)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa


class Zgloszenie(models.Model):
    STATUS_RODZAJ = {
        (1, 'Nowy'),                    #| <- Start projektu
        (2, 'Otwarty'),                 #| <- Przyjęcie lub przydzielenie zadania dla serwisanta
        (3, 'Czeka na wyjaśnienie'),    #| <- Aby zawiesić zgłoszenie - wybiera serwisant
        (4, 'Wykonany'),                #| <- Sygnalizacja przez serwisanta że zadanie zostało wykonane
        (5, 'Zamknięty'),               #| <- Zamyka całość zleceniodawca gdy serwisant zaznaczył status na WYKONANE
        (6, 'Anulowany')                #| <- Anulowanie zadania przez zamawiającego lub przełożonego
    }

    data_zgloszenia = models.DateField('data zgłoszenia')                                                           #| <-- Etap I - Zgłoszenie
    czas_zgloszenia = models.TimeField('czas zgłoszenia')                                                           #| <-- Etap I - Zgłoszenie
    temat_zgloszenia = models.CharField(max_length=400, unique=False)                                               #| <-- Etap I - Zgłoszenie
    opis_zgloszenia = models.TextField()                                                                            #| <-- Etap I - Zgłoszenie
    zglaszajacy = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='zglaszajacy')                    #| <-- Etap I - Zgłoszenie
    rodzaj_usterki = models.ForeignKey(RodzajUsterki, on_delete=models.CASCADE, default=1)                          #| <-- Etap I - Zgłoszenie  | <-- Etap II - Przydzielenie
    urzadzenie = models.ForeignKey(Urzadzenie, on_delete=models.CASCADE, default=1)                                 #| <-- Etap I - Zgłoszenie
    status = models.IntegerField(default=1, choices=STATUS_RODZAJ, unique=False)                                    #| <-- Etap I - Zgłoszenie  | <-- Etap II - Przydzielenie
    data_otwarcia = models.DateField('data otwarcia', default='1900-01-01', blank=True, null=True)                  #                           | <-- Etap II - Przydzielenie
    czas_otwarcia = models.TimeField('czas otwarcia', default='00:00', blank=True, null=True)                       #                           | <-- Etap II - Przydzielenie
    serwisant = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='serwisant', blank=True, null=True) #                           | <-- Etap II - Przydzielenie
    data_zamkniecia = models.DateField('data zamknięcia', default='1900-01-01', blank=True, null=True)              #                                                           | <-- Etap III - Zamknięcie
    czas_zamkniecia = models.TimeField('czas zamknięcia', default='00:00', blank=True, null=True)                   #                                                           | <-- Etap III - Zamknięcie
    data_wykonania = models.DateField('data wykonania', default='1900-01-01', blank=True, null=True)              #                                                           | <-- Etap III - Zamknięcie
    czas_wykonania = models.TimeField('czas wykonania', default='00:00', blank=True, null=True)                   #                                                           | <-- Etap III - Zamknięcie
    data_wstrzymania = models.DateField('data wstrzymania', default='1900-01-01', blank=True, null=True)
    czas_wstrzymania = models.TimeField('czas wstrzymania', default='00:00', blank=True, null=True)
    data_wznowienia = models.DateField('data wznowienia', default='1900-01-01', blank=True, null=True)
    czas_wznowienia = models.TimeField('czas wznowienia', default='00:00', blank=True, null=True)

    def __str__(self):
        return self.temat_zgloszenia


class Comments(models.Model):
    data_wpisu = models.DateField('data wpisu')
    czas_wpisu = models.TimeField('czas wpisu')
    zgloszenie = models.ForeignKey(Zgloszenie, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='autor')
    tresc = models.TextField()

    def __str__(self):
        return str(self.data_wpisu)

