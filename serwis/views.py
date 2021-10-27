from django.shortcuts import render, redirect
from .models import Autor, RodzajUsterki, Urzadzenie, Serwisant
from .forms import RodzajUsterkiForm, UrzadzenieForm, SerwisantForm
from datetime import datetime
from django.contrib.auth.decorators import login_required


#---------------------------------------------------
# pobieranie informacji o osobie zalogowaniej
#---------------------------------------------------
def get_author(user):
    qs = Autor.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


#---------------------------------------------------
#  Formularze Rodzajów Usterek
#---------------------------------------------------
#@login_required
def nowy_RodzajUsterek(request):
    form_RodzajUsterki = RodzajUsterkiForm(request.POST or None, request.FILES or None)
    rodzaj_usterki = RodzajUsterki.objects.all().order_by('rodzaj_usterki')

    if form_RodzajUsterki.is_valid():
        form_RodzajUsterki.save()
        return redirect(nowy_RodzajUsterek)

    context = {
        'form_RodzajUsterki': form_RodzajUsterki,
        'rodzaj_usterki': rodzaj_usterki
    }
    return render(request, 'serwis/nowy_rodzaj_usterki.html', context)


#---------------------------------------------------
#  Formularz do wprowadzania Maszyn i Urządzeń do bazy
#---------------------------------------------------
#@login_required
def nowe_Urzadzenie(request):
    form_Urzadzenia = UrzadzenieForm(request.POST or None, request.FILES or None)
    urzadzenia = Urzadzenie.objects.all().order_by('nazwa_urzadzenia')

    #test = request.POST.get('nazwa_urzadzenia')
    #print('test --> ', test)

    if form_Urzadzenia.is_valid():
        form_Urzadzenia.save()
        return redirect(nowe_Urzadzenie)

    context = {
        'form_Urzadzenia': form_Urzadzenia,
        'urzadzenia': urzadzenia
    }
    return render(request, 'serwis/nowe_urzadzenia.html', context)


#---------------------------------------------------
#  Formularz do serwisantów
#---------------------------------------------------
#@login_required
def nowy_serwisant(request):
    form_serwisant = SerwisantForm(request.POST or None, request.FILES or None)
    serwisant = Serwisant.objects.all().order_by('nazwisko')

    if form_serwisant.is_valid():
        form_serwisant.save()
        return redirect(nowy_serwisant)

    context = {
        'form_serwisant': form_serwisant,
        'serwisant': serwisant,
    }
    return render(request, 'serwis/nowy_serwisant.html', context)


