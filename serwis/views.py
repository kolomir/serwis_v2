from django.shortcuts import render, redirect
from .models import Autor, RodzajUsterki, Urzadzenie, Serwisant, Zgloszenie
from .forms import RodzajUsterkiForm, UrzadzenieForm, SerwisantForm, ZgloszeniForm
from datetime import datetime
from django.utils import timezone
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


#---------------------------------------------------
#  Formularz nowego zgłoszenia
#---------------------------------------------------
#@login_required
def nowe_zgloszenie(request):
    form_zgloszenie = ZgloszeniForm(request.POST or None, request.FILES or None)
    rodzaj_usterki = RodzajUsterki.objects.filter(aktywny=True).order_by('rodzaj_usterki')
    urzadzenie = Urzadzenie.objects.filter(aktywny=True).order_by('nazwa_urzadzenia')
    serwisant = Serwisant.objects.filter(aktywny=True).order_by('nr_serwisanta')
    zglaszajacy3 = get_author(request.user)
    zgloszenia = Zgloszenie.objects.filter(zglaszajacy=zglaszajacy3).order_by('data_zgloszenia')

    data_zgl = request.POST.get('data_zgloszenia')
    czas_zgl = request.POST.get('czas_zgloszenia')
    temat = request.POST.get('temat_zgloszenia')
    opis = request.POST.get('opis_zgloszenia')
    zglaszajacy2 = get_author(request.user)
    usterka = request.POST.get('rodzaj_usterki')
    if usterka is None:
        usterka1 = 'Nie wybrano maszyny'
    else:
        usterka1 = RodzajUsterki.objects.get(id=usterka)
    maszyna = request.POST.get('urzadzenie')
    if maszyna is None:
        maszyna1 = 'Nie wybrano maszyny'
    else:
        maszyna1 = Urzadzenie.objects.get(id=maszyna)
    status1 = 1
    #--------------------------------------------------------------------------------
    data_otwarcia1 = '1900-01-01'
    czas_otwarcia1 = '00:00'
    serwisant1 = 1
    data_zamkniecia1 = '1900-01-01'
    czas_zamkniecia1 = '00:00'

#- STREFA TESTU ----------------------------------------------------------------------
    print('data --> ', data_zgl)
    print('czas --> ', czas_zgl)
    print('temat --> ', temat)
    print('opis --> ', opis)
    print('zglaszajacy --> ', zglaszajacy2)
    print('Usterka --> ', usterka)
    print('Usterka1 --> ', usterka1)
    print('urzadzenie --> ', maszyna)
    print('urzadzenie1 --> ', maszyna1)
    if status1 is not None and int(status1) == 1:
        print('status --> Nowy')
    else:
        print('status --> Nieznany')
    print('-------------------------------------------')
    print('data_otwarcia --> ', data_otwarcia1)
    print('czas_otwarcia --> ', czas_otwarcia1)
    print('serwisant --> ', serwisant1)
    print('data_zamkniecia --> ', data_zamkniecia1)
    print('czas_zamkniecia --> ', czas_zamkniecia1)


    data_teraz = datetime.now()
    data_zgloszenia = data_teraz.strftime("%Y-%m-%d")
    czas_teraz = timezone.now()
    czas_zgloszenia = czas_teraz.strftime("%H:%M")

#------------------------------------------------------------------------------------

    if form_zgloszenie.is_valid():
        autor = get_author(request.user)
        form_zgloszenie.instance.data_otwarcia = data_otwarcia1
        form_zgloszenie.instance.czas_otwarcia = czas_otwarcia1
        form_zgloszenie.instance.Serwisant = serwisant1
        form_zgloszenie.instance.data_zamkniecia = data_zamkniecia1
        form_zgloszenie.instance.czas_zamkniecia = czas_zamkniecia1
        form_zgloszenie.instance.Status = status1
        form_zgloszenie.instance.zglaszajacy = autor
        form_zgloszenie.instance.data_zgloszenia = request.POST.get('data_zgloszenia')
        form_zgloszenie.instance.czas_zgloszenia = request.POST.get('czas_zgloszenia')
        form_zgloszenie.save()
        return redirect(nowe_zgloszenie)

    context = {
        'form_zgloszenie': form_zgloszenie,
        'data_zgloszenia': data_zgloszenia,
        'czas_zgloszenia': czas_zgloszenia,
        'rodzaj_usterki': rodzaj_usterki,
        'urzadzenie': urzadzenie,
        'serwisant': serwisant,
        'zgloszenia': zgloszenia,
    }
    return render(request, 'serwis/nowe_zgloszenie.html', context)
    #return render(request, 'serwis/test.html', context)





