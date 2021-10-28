from django.db import models
from django.contrib.auth.models import User


class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
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
        return self.nr_serwisanta

class Status(models.Model):
    nazwa = models.CharField(max_length=40, unique=True)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa


class Zgloszenie(models.Model):
    data_zgloszenia = models.DateField('data zgłoszenia')
    czas_zgloszenia = models.TimeField('czas zgłoszenia')
    temat_zgloszenia = models.CharField(max_length=400, unique=False)
    opis_zgloszenia = models.TextField()
    zglaszajacy = models.ForeignKey(Autor, on_delete=models.CASCADE)
    rodzaj_usterki = models.ForeignKey(RodzajUsterki, on_delete=models.CASCADE, default=1)
    urzadzenie = models.ForeignKey(Urzadzenie, on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    data_otwarcia = models.DateField('data otwarcia')
    czas_otwarcia = models.TimeField('czas otwarcia')
    serwisant = models.ForeignKey(Serwisant, on_delete=models.CASCADE, default=1)
    data_zamkniecia = models.DateField('data zamknięcia')
    czas_zamkniecia = models.TimeField('czas zamknięcia')

    def __str__(self):
        return self.temat_zgloszenia


