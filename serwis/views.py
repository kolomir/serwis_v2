from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, RodzajUsterki, Urzadzenie, Serwisant, Zgloszenie, Comments
from .forms import RodzajUsterkiForm, KasujRodzajUsterki, UrzadzenieForm, KasujUrzadzenie, SerwisantForm, ZgloszeniForm, PodjecieZgloszeniaForm, CommentsForm, AnulowacZgloszenie, WykonanieZgloszenie, ZawieszenieZgloszenia
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import csv


#---------------------------------------------------
# pobieranie informacji o osobie zalogowaniej.
#---------------------------------------------------
def get_author(user):
    qs = Autor.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

#---------------------------------------------------
# inne
#---------------------------------------------------
def przerobienie_daty(data,godzina):
   (rok1, miesiac1, dzien1) = data.split("-")
   (godzina1, minuta1, sekunda1) = godzina.split(":")
   return datetime(int(rok1),int(miesiac1),int(dzien1),int(godzina1),int(minuta1),int(sekunda1))


def przerobienie_tylko_czasu(godzina):
   (godzina1, minuta1) = godzina.split(":")
   return datetime(int(godzina1),int(minuta1))


def przerobienie_tylko_daty(data):
   (rok1, miesiac1, dzien1) = data.split("-")
   return datetime(int(rok1),int(miesiac1),int(dzien1))


def czas_na_minuty(t):
    #podawany jest czas w formacie HH:MM
    h, m, s = map(int, t.split(':'))
    return h * 60 + m


#---------------------------------------------------
#  Formularze Rodzajów Usterek
#---------------------------------------------------
@login_required
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


@login_required
def edytuj_RodzajUsterek(request, id):
    wpis = get_object_or_404(RodzajUsterki, pk=id)
    form_RodzajUsterki = RodzajUsterkiForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_RodzajUsterki.is_valid():
        form_RodzajUsterki.save()
        return redirect(nowy_RodzajUsterek)

    context = {
        'form_RodzajUsterki': form_RodzajUsterki,
        'wpis':wpis,
    }
    return render(request, 'serwis/edytuj_rodzaj_usterki.html', context)


@login_required
def usun_RodzajUsterek(request, id):
    wpis = get_object_or_404(RodzajUsterki, pk=id)
    form_RodzajUsterki = KasujRodzajUsterki(request.POST or None, request.FILES or None, instance=wpis)

    if form_RodzajUsterki.is_valid():
        kasuj = form_RodzajUsterki.save(commit=False)
        kasuj.aktywny = '0'
        kasuj.save()
        return redirect(nowy_RodzajUsterek)

    context = {
        'wpis': wpis,
    }
    return render(request, 'serwis/potwierdz_rodzaj_usterki.html', context)


@login_required
def przywroc_RodzajUsterek(request, id):
    wpis = get_object_or_404(RodzajUsterki, pk=id)
    form_RodzajUsterki = KasujRodzajUsterki(request.POST or None, request.FILES or None, instance=wpis)

    if form_RodzajUsterki.is_valid():
        kasuj = form_RodzajUsterki.save(commit=False)
        kasuj.aktywny = '1'
        kasuj.save()
        return redirect(nowy_RodzajUsterek)

    context = {
        'wpis': wpis,
    }
    return render(request, 'serwis/potwierdz_rodzaj_usterki.html', context)


#---------------------------------------------------
#  Formularz do wprowadzania Maszyn i Urządzeń do bazy
#---------------------------------------------------
@login_required
def nowe_Urzadzenie(request):
    form_Urzadzenia = UrzadzenieForm(request.POST or None, request.FILES or None)
    urzadzenia = Urzadzenie.objects.all().order_by('nazwa_urzadzenia')

    if form_Urzadzenia.is_valid():
        form_Urzadzenia.save()
        return redirect(nowe_Urzadzenie)

    context = {
        'form_Urzadzenia': form_Urzadzenia,
        'urzadzenia': urzadzenia
    }
    return render(request, 'serwis/nowe_urzadzenia.html', context)


@login_required
def edytuj_Urzadzenie(request, id):
    wpis = get_object_or_404(Urzadzenie, pk=id)
    form_Urzadzenie = UrzadzenieForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_Urzadzenie.is_valid():
        form_Urzadzenie.save()
        return redirect(nowe_Urzadzenie)

    context = {
        'form_Urzadzenie': form_Urzadzenie,
        'wpis':wpis,
    }
    return render(request, 'serwis/edytuj_urzadzenia.html', context)


@login_required
def usun_Urzadzenie(request, id):
    wpis = get_object_or_404(Urzadzenie, pk=id)
    form_Urzadzenie = KasujUrzadzenie(request.POST or None, request.FILES or None, instance=wpis)

    if form_Urzadzenie.is_valid():
        kasuj = form_Urzadzenie.save(commit=False)
        kasuj.aktywny = '0'
        kasuj.save()
        return redirect(nowe_Urzadzenie)

    context = {
        'wpis': wpis,
    }
    return render(request, 'serwis/potwierdz_urzadzenie.html', context)


@login_required
def przywroc_Urzadzenie(request, id):
    wpis = get_object_or_404(Urzadzenie, pk=id)
    form_Urzadzenie = KasujUrzadzenie(request.POST or None, request.FILES or None, instance=wpis)

    if form_Urzadzenie.is_valid():
        kasuj = form_Urzadzenie.save(commit=False)
        kasuj.aktywny = '1'
        kasuj.save()
        return redirect(nowe_Urzadzenie)

    context = {
        'wpis': wpis,
    }
    return render(request, 'serwis/potwierdz_urzadzenie.html', context)



#---------------------------------------------------
#  Zestawienie zamkniętych zleceń
#---------------------------------------------------
def wpis_zamkniete(request):
    zamkniete_zgloszenia = Zgloszenie.objects.filter(status__gte=5).order_by('-data_zgloszenia', 'czas_zgloszenia')

    context = {
        'zamkniete_zgloszenia': zamkniete_zgloszenia,
    }

    return render(request, 'serwis/zamkniete.html', context)


#---------------------------------------------------
#  Zestawienie zamkniętych zleceń - szczegóły
#---------------------------------------------------
def wpis_zamkniete_szczegoly(request, id):
    zgloszenia = get_object_or_404(Zgloszenie, pk=id)

    # - komentarze --------------------------
    komentarze = Comments.objects.filter(zgloszenie=zgloszenia.id).order_by('data_wpisu')


    context = {
        'zgloszenia': zgloszenia,
        'komentarze': komentarze,
    }

    return render(request, 'serwis/zgloszenie_hist.html', context)


#---------------------------------------------------
#  Wpisy
#---------------------------------------------------
def wpisy(request):
    nowe_zgloszenia = Zgloszenie.objects.filter(status=1).order_by('data_zgloszenia', 'czas_zgloszenia')
    otwarte_zgloszenia = Zgloszenie.objects.filter(status__gte=2,status__lte=4).order_by('data_zgloszenia', 'czas_zgloszenia')
    #- czy serwisant ---------
    if request.user.is_authenticated:
        zglaszajacy_wpisy = get_author(request.user)
        lista_userow = get_user_model()
        zalogowany_user = get_object_or_404(lista_userow, username__exact=zglaszajacy_wpisy)
        serwisy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
        serwisant = int(serwisy.serwis)
        zgloszenia_zglaszajacy = Zgloszenie.objects.filter(status__gte=2,status__lte=4).filter(zglaszajacy=zglaszajacy_wpisy.id).order_by('status')
        zgloszenia_serwis = Zgloszenie.objects.filter(serwisant_id=zglaszajacy_wpisy.id).filter(status__gte=2,status__lt=4).order_by('status','data_zgloszenia', 'czas_zgloszenia')
    else:
        zgloszenia_zglaszajacy = ""
        zgloszenia_serwis = ""
        serwisant = ""

    zgloszenia = Zgloszenie.objects.filter(status__lte=4).order_by('data_zgloszenia', 'czas_zgloszenia')

    context = {
        'zgloszenia': zgloszenia,
        'nowe_zgloszenia': nowe_zgloszenia,
        'otwarte_zgloszenia': otwarte_zgloszenia,
        'zgloszenia_zglaszajacy': zgloszenia_zglaszajacy,
        'zgloszenia_serwis': zgloszenia_serwis,
        'serwisant': serwisant,
    }
    return render(request, 'serwis/wpisy.html', context)


#---------------------------------------------------
#  Wpis - szczegóły
#---------------------------------------------------
@login_required
def wpis_szczegoly(request, id):
    zgloszenia = get_object_or_404(Zgloszenie, pk=id)

    # - czy serwisant ---------
    zglaszajacy_wpisy = get_author(request.user)
    lista_userow = get_user_model()
    zalogowany_user = get_object_or_404(lista_userow, username__exact=zglaszajacy_wpisy)
    serwisy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    serwisant = int(serwisy.serwis)

    # - forms - podjęcie zgłoszenia -----------------
    form_podjecie_zgloszenia = PodjecieZgloszeniaForm(request.POST or None, request.FILES or None, instance=zgloszenia)

    # - forms - zawieszenie/wznownienie zgłoszenia --------------
    form_zawieszenie_zgloszenia = ZawieszenieZgloszenia(request.POST or None, request.FILES or None, instance=zgloszenia)

    # - forms - wykonanie zgłoszenia ----------------
    form_wykonanie_zgloszenia = WykonanieZgloszenie(request.POST or None, request.FILES or None, instance=zgloszenia)

    # - forms - komentarze --------------------------
    komentarze = Comments.objects.filter(zgloszenie=zgloszenia.id).order_by('data_wpisu')
    form_komentarze = CommentsForm(request.POST or None, request.FILES or None)

    # =================================================================
    # - STREFA TESTU --------------------------------------------------
    # =================================================================
    data_zgl = request.POST.get('data_przekazana')
    czas_zgl = request.POST.get('czas_przekazany')
    status = request.POST.get('status')

    data_com = request.POST.get('data_wpisu')
    czas_com = request.POST.get('czas_wpisu')
    tresci = request.POST.get('tresc')
    zgloszenie_com = request.POST.get('zgloszenie')

    print('--- TEST - ZGLOSZENIE ------------------------------')
    print('----------------------------------------------------')
    print('data --> ', data_zgl)
    print('czas --> ', czas_zgl)
    print('status --> ', status)
    print('----------------------------------------------------')
    print('--- TEST - KOMENTARZE ------------------------------')
    print('----------------------------------------------------')
    print('data komentarza --> ', data_com)
    print('czas komentarza --> ', czas_com)
    print('tersc --> ', tresci)
    print('zgloszenie --> ', zgloszenie_com)
    # -----------------------------------------------------------------

    data_teraz = datetime.now()
    data_przekazana = data_teraz.strftime("%Y-%m-%d")
    czas_teraz = timezone.now()
    czas_przekazany = czas_teraz.strftime("%H:%M")
    #'''
    if request.method == 'POST' and 'btn_form_podejmij' in request.POST:
        data_zgloszenie = request.POST.get('data_zgloszenia')
        czas_zgloszenie = request.POST.get('czas_zgloszenia')
        print('--- zgloszenie ------------------------------')
        print('data_zgloszenie: ', data_zgloszenie)
        print('czas_zgloszenie: ', czas_zgloszenie)

        przerobiony_czas_zgloszenia = przerobienie_daty(data_zgloszenie, czas_zgloszenie)
        przerobiony_czas_podjecia = przerobienie_daty(data_zgl, czas_zgl)
        czas_r = przerobiony_czas_podjecia - przerobiony_czas_zgloszenia
        dni = czas_r.days
        godziny = czas_r.seconds / 60 / 60
        minuty = czas_r.seconds / 60
        sek = czas_r.seconds

        #przerobiony_tylko_czas_zgloszenia = przerobienie_tylko_czasu(czas_zgloszenie)
        #przerobiony_tylko_czas_podjecia = przerobienie_tylko_czasu(czas_zgl)
        #tylko_czas = przerobiony_tylko_czas_podjecia - przerobiony_tylko_czas_zgloszenia
        #czas_w_minutach = czas_na_minuty(str(czas_r))

        print('--- dni ------------------------------')
        print('dni:', dni)
        print('godziny:', godziny)
        print('minuty:', minuty)
        print('sek:', sek)
        print('nr1 minęło dni: %s, godzin: %d, minut: %d' % (czas_r.days, czas_r.seconds / 3600, (czas_r.seconds % 3600) / 60))
        print('--- czas zgloszenia ------------------------------')
        print('przerobiony_czas_zgloszenia: ', przerobiony_czas_zgloszenia)
        print('--- czas podjecia ------------------------------')
        print('przerobiony_czas_podjecia: ', przerobiony_czas_podjecia)
        print('--- czas_r ------------------------------')
        print('czas_r: ', czas_r)
        print('--- czas_w_minutach ------------------------------')
        test_data_zgl = przerobienie_tylko_daty(data_zgl)
        test_data_podj = przerobienie_tylko_daty(data_zgloszenie)
        test_data = test_data_zgl-test_data_podj
        print(test_data)
        if test_data >= timedelta(days=1):
            #test_dni = timedelta.test_data.day
            godz = test_data.days * 24
            #czas_w_minutach = czas_na_minuty(str(czas_r))
            #print('czas_w_minutach:', czas_w_minutach)
            print('godz:', godz)
            print('dni:', test_data.days)
            #rint('czas:', tylko_czas)
            print('jest')

        #print('czas_w_minutach: ', czas_w_minutach)

        if form_podjecie_zgloszenia.is_valid():
            autor = get_author(request.user)
            form_podjecie_zgloszenia.instance.serwisant = autor
            form_podjecie_zgloszenia.instance.data_otwarcia = request.POST.get('data_przekazana')
            form_podjecie_zgloszenia.instance.czas_otwarcia = request.POST.get('czas_przekazany')
            form_podjecie_zgloszenia.instance.status = status
            print('>>-- Podjecie --<<')
            print(
                'autor:', autor,
                ' ; autor.id:', autor.id,
                ' ; data_otwarcia:', data_przekazana,
                ' ; czas_otwarcia:', czas_przekazany,
                ' ; status:', status)
            print('>>---------------<<')
            #form_podjecie_zgloszenia.save()
            return redirect(wpisy)

    if request.method == 'POST' and 'btn_form_wykonane' in request.POST:

        if form_wykonanie_zgloszenia.is_valid():
            form_wykonanie_zgloszenia.instance.data_wykonania = request.POST.get('data_przekazana')
            form_wykonanie_zgloszenia.instance.czas_wykonania = request.POST.get('czas_przekazany')
            form_wykonanie_zgloszenia.instance.status = status
            print('>>-- Wykonanie --<<')
            print(
                'data_otwarcia:', data_przekazana,
                ' ; czas_otwarcia:', czas_przekazany,
                ' ; status:', status,
                )
            print('>>---------------<<')
            form_wykonanie_zgloszenia.save()
            return redirect(wpisy)

    if request.method == 'POST' and 'btn_form_wstrzymane' in request.POST:
# TODO: jeżeli jest wstrzymane zgłoszenie z jakichś powodów to może wyłączyć również komentarze na ten czas.
        if form_wykonanie_zgloszenia.is_valid():
            form_wykonanie_zgloszenia.instance.status = status
            print('>>-- Wstrzymanie --<<')
            print(
                'data_otwarcia:', data_przekazana,
                ' ; czas_otwarcia:', czas_przekazany,
                ' ; status:', status)
            print('>>-----------------<<')
            form_wykonanie_zgloszenia.save()
            return redirect(wpisy)

    if request.method == 'POST' and 'btn_form_przywrocenie' in request.POST:
# TODO: po przywróceniu zlecenia komentarze powinny wrócić oczywiście.
        if form_wykonanie_zgloszenia.is_valid():
            form_wykonanie_zgloszenia.instance.status = status
            print('>>-- Przywrócenie --<<')
            print(
                'data_otwarcia:', data_przekazana,
                ' ; czas_otwarcia:', czas_przekazany,
                ' ; status:', status)
            print('>>------------------<<')
            form_wykonanie_zgloszenia.save()
            return redirect(wpisy)
# TODO: zminić sposób zatwierdzania. Powinna być strona uperniająca z potwierdzeniem tak jak przy anulowaniu zlecenia
    if request.method == 'POST' and 'btn_form_zakonczenie' in request.POST:

        if form_wykonanie_zgloszenia.is_valid():
            form_wykonanie_zgloszenia.instance.data_zamkniecia = request.POST.get('data_przekazana')
            form_wykonanie_zgloszenia.instance.czas_zamkniecia = request.POST.get('czas_przekazany')
            form_wykonanie_zgloszenia.instance.status = status
            print('>>-- Zamknięcie --<<')
            print(
                'data_otwarcia:', data_przekazana,
                ' ; czas_otwarcia:', czas_przekazany,
                ' ; status:', status)
            print('>>----------------<<')
            form_wykonanie_zgloszenia.save()
            return redirect(wpisy)
    #'''
    if request.method == 'POST':# and 'btn_form_komentarz' in request.POST:
        # - forms - komentarze --------------------------
        #form_komentarze = CommentsForm(request.POST or None, request.FILES or None)
        
        if form_komentarze.is_valid():
            autor = get_author(request.user)
            form_komentarze.instance.autor = autor
            form_komentarze.instance.data_wpisu = request.POST.get('data_wpisu')
            form_komentarze.instance.czas_wpisu = request.POST.get('czas_wpisu')
            print(
                '11111111111111111',
                'autor:', autor,
                ' ; autor.id:', autor.id,
                ' ; data_wpisu:', data_przekazana,
                ' ; czas_wpisu:', czas_przekazany,
                ' ; tresc:', tresci,
                ' ; zgloszenie:', zgloszenie_com)
            form_komentarze.save()
    #'''

    context = {
        'zgloszenia': zgloszenia,
        'form_podjecie_zgloszenia': form_podjecie_zgloszenia,
        'data_przekazana': data_przekazana,
        'czas_przekazany': czas_przekazany,
        'serwisant': serwisant,
        'komentarze': komentarze,
        'form_komentarze': form_komentarze,
    }
    return render(request, 'serwis/zgloszenie.html', context)


#---------------------------------------------------
#  Formularz nowego zgłoszenia
#---------------------------------------------------
@login_required
def nowe_zgloszenie(request):
    form_zgloszenie = ZgloszeniForm(request.POST or None, request.FILES or None)
    rodzaj_usterki = RodzajUsterki.objects.filter(aktywny=True).order_by('rodzaj_usterki')
    urzadzenie = Urzadzenie.objects.filter(aktywny=True).order_by('nazwa_urzadzenia')
    zglaszajacy_wpisy = get_author(request.user)
    zgloszenia = Zgloszenie.objects.filter(status__lt=5, zglaszajacy__exact=zglaszajacy_wpisy)
    #- czy serwisant ---------
    lista_userow = get_user_model()
    zalogowany_user = get_object_or_404(lista_userow, username__exact=zglaszajacy_wpisy)
    serwisy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    wyslij = int(serwisy.serwis)


    #-STREFA TESTU ---------------------------------------------------
    data_zgl = request.POST.get('data_zgloszenia')
    czas_zgl = request.POST.get('czas_zgloszenia')
    temat = request.POST.get('temat_zgloszenia')
    opis = request.POST.get('opis_zgloszenia')
    zglaszajacy2 = get_author(request.user)

    print('--- TEST -------------------------------------------')
    print('data --> ', data_zgl)
    print('czas --> ', czas_zgl)
    print('temat --> ', temat)
    print('opis --> ', opis)
    print('zglaszajacy --> ', zglaszajacy2)
    print('obj --> ', zalogowany_user.id)
    print('obj2 --> ', serwisy.serwis)
    print('wyslij --> ', wyslij)

    #-----------------------------------------------------------------

    data_teraz = datetime.now()
    data_zgloszenia = data_teraz.strftime("%Y-%m-%d")
    czas_teraz = timezone.now()
    czas_zgloszenia = czas_teraz.strftime("%H:%M")

    if form_zgloszenie.is_valid():
        autor = get_author(request.user)
        form_zgloszenie.instance.zglaszajacy = autor
        form_zgloszenie.instance.data_zgloszenia = request.POST.get('data_zgloszenia')
        form_zgloszenie.instance.czas_zgloszenia = request.POST.get('czas_zgloszenia')
        form_zgloszenie.save()
        return redirect(wpisy)

    context = {
        'form_zgloszenie': form_zgloszenie,
        'data_zgloszenia': data_zgloszenia,
        'czas_zgloszenia': czas_zgloszenia,
        'rodzaj_usterki': rodzaj_usterki,
        'urzadzenie': urzadzenie,
        'zgloszenia': zgloszenia,
        'wyslij': wyslij,
    }
    return render(request, 'serwis/nowe_zgloszenie.html', context)
    #return render(request, 'serwis/test.html', context)


#---------------------------------------------------
#  Anulowanie zgłoszenia
#---------------------------------------------------
@login_required
def anuluj_zgloszenie(request, id):
    wpis = get_object_or_404(Zgloszenie, pk=id)
    form_wpis = AnulowacZgloszenie(request.POST or None, request.FILES or None, instance=wpis)

    data_teraz = datetime.now()
    data_zamkniecia = data_teraz.strftime("%Y-%m-%d")
    czas_teraz = timezone.now()
    czas_zamkniecia = czas_teraz.strftime("%H:%M")
    status = 6

    if form_wpis.is_valid():
        #kasuj = form_wpis.save(commit=False)
        #kasuj.status = status
        #kasuj.data_zamkniecia = request.POST.get('data_zamkniecia')
        #kasuj.czas_zamkniecia = request.POST.get('czas_zamkniecia')
        #kasuj.save()
        form_wpis.instance.status = request.POST.get('status')
        form_wpis.instance.data_zamkniecia = request.POST.get('data_zamkniecia')
        form_wpis.instance.czas_zamkniecia = request.POST.get('czas_zamkniecia')
        form_wpis.save()
        return redirect(wpisy)


    context = {
        'wpis': wpis,
        'data_zamkniecia': data_zamkniecia,
        'czas_zamkniecia': czas_zamkniecia,
    }
    return render(request, 'serwis/potwierdz_anuluj_zgloszenie.html', context)

#TODO: można dodać tabelę dodatkową do opisów po wykonaniu zlecenia. Innym pomysłem jest dodanie pozycji jako ostatni komentarz.
#TODO: zminić sposób zatwierdzania. Powinna być strona uperniająca z potwierdzeniem tak jak przy anulowaniu zlecenia
#---------------------------------------------------
#  Zamknięcie zgłoszenia
#---------------------------------------------------
@login_required
def zakoncz_zgloszenie(request, id):
    wpis = get_object_or_404(Zgloszenie, pk=id)
    form_wpis = AnulowacZgloszenie(request.POST or None, request.FILES or None, instance=wpis)

    data_teraz = datetime.now()
    data_przekazana = data_teraz.strftime("%Y-%m-%d")
    czas_teraz = timezone.now()
    czas_przekazany = czas_teraz.strftime("%H:%M")
    status = 5

    if form_wpis.is_valid():
        #kasuj = form_wpis.save(commit=False)
        print('>>-- Zamknięcie --<<')
        print(
            'data_otwarcia:', data_przekazana,
            ' ; czas_otwarcia:', czas_przekazany,
            ' ; status:', status)
        print('>>----------------<<')
        form_wpis.instance.status = status
        form_wpis.instance.data_zamkniecia = request.POST.get('data_przekazana')
        form_wpis.instance.czas_zamkniecia = request.POST.get('czas_przekazany')
        form_wpis.save()
        return redirect(wpisy)


    context = {
        'wpis': wpis,
        'data_przekazana': data_przekazana,
        'czas_przekazany': czas_przekazany,
    }
    return render(request, 'serwis/potwierdz_zakoncz_zgloszenie.html', context)


#---------------------------------------------------
#  Formularz logowania
#---------------------------------------------------
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info( request, f"Witaj {username}! Właśnie się zalogowałeś.")
                return redirect("/")
            else:
                messages.error(request, f"Błędny login lub hasło")
        else:
            messages.error(request, f"- Błędny login lub hasło -")
    form = AuthenticationForm()

    context = {
        "form": form
    }
    return render(request, "serwis/login.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "Właśnie się wylogowałeś")
    return redirect(wpisy)


#---------------------------------------------------
#  Eksport danych - Czas reakcji
#---------------------------------------------------
def is_valid_queryparam(param):
    return param != '' and param is not None


def exp_czas_reakcji(request):
    #qs = Zgloszenie.objects.filter(status__gte=2).filter(status__lte=5)

    data_od = request.GET.get('data_od')
    data_do = request.GET.get('data_do')
    eksport = request.GET.get('eksport')

    tylko_zamkniete = request.GET.get('zamkniete')
    if tylko_zamkniete == 'tak':
        qs = Zgloszenie.objects.filter(status=5)
    else:
        qs = Zgloszenie.objects.filter(status__gte=2).filter(status__lte=5)
    print('test11', tylko_zamkniete)

    if is_valid_queryparam(data_od):
        qs = qs.filter(data_zgloszenia__gte=data_od)
    if is_valid_queryparam(data_do):
        qs = qs.filter(data_zgloszenia__lte=data_do)

    test = request.GET.get('eksport')
    #eksport = 'on'
    print('test ', test)
    print('data od', data_od)

    if eksport == "on":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = "rap_czas_reakcji.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'temat zgloszenia',
                'zglaszajacy',
                'Data zgłoszenia',
                'Data podjęcia ',
                'Serwisant',
                'Status',
                'Czas reakcji/dni',
                'Czas reakcji/czas',
            ]
        )
        for obj in qs:
            przerobiony_czas_zgloszenia = przerobienie_daty(str(obj.data_zgloszenia), str(obj.czas_zgloszenia))
            przerobiony_czas_otwarcia = przerobienie_daty(str(obj.data_otwarcia), str(obj.czas_otwarcia))
            czas_reakcji = przerobiony_czas_otwarcia - przerobiony_czas_zgloszenia
            czas_reakcji_dni = czas_reakcji.days
            czas_reakcji_czas = '%d:%d' % (czas_reakcji.seconds / 3600, (czas_reakcji.seconds % 3600) / 60)
            writer.writerow(
                [
                    obj.temat_zgloszenia,
                    obj.zglaszajacy,
                    obj.data_zgloszenia,
                    obj.data_otwarcia,
                    obj.serwisant,
                    obj.status,
                    czas_reakcji_dni,
                    czas_reakcji_czas,
                ]
            )
        return response
    context = {
        'queryset': qs,
    }
    return render(request, 'serwis/exp_czas_reakcji.html', context)


#---------------------------------------------------
#  Eksport danych - Całkowity czas trwania zadania
#---------------------------------------------------
def exp_pelny_czas_zadania(request):
    qs = Zgloszenie.objects.filter(status=5)

    data_od = request.GET.get('data_od')
    data_do = request.GET.get('data_do')
    eksport = request.GET.get('eksport')

    if is_valid_queryparam(data_od):
        qs = qs.filter(data_zgloszenia__gte=data_od)
    if is_valid_queryparam(data_do):
        qs = qs.filter(data_zgloszenia__lte=data_do)

    if eksport == "on":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = "rap_pelny_czas_zadania.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'temat zgloszenia',
                'zglaszajacy',
                'Data zgłoszenia',
                'Data zamknięcia',
                'Serwisant',
                'Status',
                'Czas zgłoszenia/dni',
                'Czas zgłoszenia/czas',
            ]
        )
        for obj in qs:
            przerobiony_czas_zgloszenia = przerobienie_daty(str(obj.data_zgloszenia), str(obj.czas_zgloszenia))
            przerobiony_czas_zamkniecia = przerobienie_daty(str(obj.data_zamkniecia), str(obj.czas_zamkniecia))
            czas_zgloszenia = przerobiony_czas_zamkniecia - przerobiony_czas_zgloszenia
            czas_zgloszenia_dni = czas_zgloszenia.days
            czas_zgloszenia_czas = '%d:%d' % (czas_zgloszenia.seconds / 3600, (czas_zgloszenia.seconds % 3600) / 60)
            writer.writerow(
                [
                    obj.temat_zgloszenia,
                    obj.zglaszajacy,
                    obj.data_zgloszenia,
                    obj.data_zamkniecia,
                    obj.serwisant,
                    obj.status,
                    czas_zgloszenia_dni,
                    czas_zgloszenia_czas,
                ]
            )
        return response
    context = {
        'queryset': qs,
    }
    return render(request, 'serwis/exp_pelny_czas_zadania.html', context)


#---------------------------------------------------
#  Eksport danych - Czas zawieszenia zadań
#---------------------------------------------------
def exp_czas_zawieszenia(request):
    qs = Zgloszenie.objects.filter(status__gte=2).filter(status__lte=5)

    data_teraz = datetime.now()
    data_przekazana = data_teraz.strftime("%Y-%m-%d")
    czas_teraz = timezone.now()
    czas_przekazany = czas_teraz.strftime("%H:%M:%S")

    data_od = request.GET.get('data_od')
    data_do = request.GET.get('data_do')
    eksport = request.GET.get('eksport')

    if is_valid_queryparam(data_od):
        qs = qs.filter(data_zgloszenia__gte=data_od)
    if is_valid_queryparam(data_do):
        qs = qs.filter(data_zgloszenia__lte=data_do)

    if eksport == "on":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = "rap_czas_zawieszenia.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'temat zgloszenia',
                'zglaszajacy',
                'Data zgłoszenia',
                'Data zawieszenia',
                'Data wznowienia',
                'Serwisant',
                'Status',
                'Czas zgłoszenia/dni',
                'Czas zgłoszenia/czas',
            ]
        )
        for obj in qs:
            if str(obj.data_wstrzymania) == '1900-01-01':
                print('pominac')
            else:
                if str(obj.data_wznowienia) == '1900-01-01':
                    data_wznowienia = str(data_przekazana)
                    czas_wznowienia = str(czas_przekazany)
                else:
                    data_wznowienia = str(obj.data_wznowienia)
                    czas_wznowienia = str(obj.czas_wznowienia)

                print('data_wznowienia: ', data_wznowienia, '; czas_wznowienia: ', czas_wznowienia)

                przerobiony_czas_wstrzymania = przerobienie_daty(str(obj.data_wstrzymania), str(obj.czas_wstrzymania))
                przerobiony_czas_wznowienia = przerobienie_daty(str(data_wznowienia), str(czas_wznowienia))
                czas_wstrzymania_prac = przerobiony_czas_wznowienia - przerobiony_czas_wstrzymania
                czas_wstrzymania_prac_dni = czas_wstrzymania_prac.days
                czas_wstrzymania_prac_czas = '%d:%d' % (czas_wstrzymania_prac.seconds / 3600, (czas_wstrzymania_prac.seconds % 3600) / 60)
                print('obliczyc')
                writer.writerow(
                    [
                        obj.temat_zgloszenia,
                        obj.zglaszajacy,
                        obj.data_zgloszenia,
                        obj.data_wstrzymania,
                        data_wznowienia,
                        obj.serwisant,
                        obj.status,
                        czas_wstrzymania_prac_dni,
                        czas_wstrzymania_prac_czas,
                    ]
                )
        return response
    context = {
        'queryset': qs,
    }
    return render(request, 'serwis/exp_czas_zawieszenia.html', context)


#---------------------------------------------------
#---------------------------------------------------
#  testy
#---------------------------------------------------
#---------------------------------------------------
def autorzy(request):
    User = get_user_model()
    qs = User.objects.all()
    serwis = Autor.objects.all()

    context = {
        'qs': qs,
        'serwis': serwis,
    }

    return render(request, 'serwis/test.html', context)


#---------------------------------------------------
#  Formularz do serwisantów
#---------------------------------------------------
#@login_required
def nowy_serwisant(request):
    form_serwisant = SerwisantForm(request.POST or None, request.FILES or None)
    serwisant = Serwisant.objects.all().order_by('nazwisko')
    User = get_user_model()
    uzytkownik = User.objects.all()

    if form_serwisant.is_valid():
        form_serwisant.save()
        return redirect(nowy_serwisant)

    context = {
        'form_serwisant': form_serwisant,
        'serwisant': serwisant,
        'uzytkownik': uzytkownik,
    }
    return render(request, 'serwis/nowy_serwisant.html', context)