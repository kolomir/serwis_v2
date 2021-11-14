from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, RodzajUsterki, Urzadzenie, Serwisant, Zgloszenie, Comments
from .forms import RodzajUsterkiForm, UrzadzenieForm, SerwisantForm, ZgloszeniForm, PodjecieZgloszeniaForm, CommentsForm
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


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


#---------------------------------------------------
#  Formularz do wprowadzania Maszyn i Urządzeń do bazy
#---------------------------------------------------
@login_required
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
#  Wpisy
#---------------------------------------------------
def wpisy(request):
    zgloszenia = Zgloszenie.objects.filter(status=1).order_by('data_zgloszenia', 'czas_zgloszenia')
    #- czy serwisant ---------
    zglaszajacy_wpisy = get_author(request.user)
    lista_userow = get_user_model()
    zalogowany_user = get_object_or_404(lista_userow, username__exact=zglaszajacy_wpisy)
    serwisy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    wyslij = int(serwisy.serwis)

    twoje_zgloszenia = Zgloszenie.objects.filter(serwisant_id=zglaszajacy_wpisy.id).order_by('status','data_zgloszenia', 'czas_zgloszenia')

    context = {
        'zgloszenia': zgloszenia,
        'twoje_zgloszenia': twoje_zgloszenia,
        'wyslij': wyslij,
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
    wyslij = int(serwisy.serwis)

    # - forms - podjęcie zgłoszenia -----------------
    form_podjecie_zgloszenia = PodjecieZgloszeniaForm(request.POST or None, request.FILES or None, instance=zgloszenia)

    # - forms - komentarze --------------------------
    komentarze = Comments.objects.filter(zgloszenie=zgloszenia.id).order_by('data_wpisu')
    form_komentarze = CommentsForm(request.POST or None, request.FILES or None)

    # =================================================================
    # - STREFA TESTU --------------------------------------------------
    # =================================================================
    data_zgl = request.POST.get('data_otwarcia')
    czas_zgl = request.POST.get('czas_otwarcia')
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
    data_otwarcia = data_teraz.strftime("%Y-%m-%d")
    czas_teraz = timezone.now()
    czas_otwarcia = czas_teraz.strftime("%H:%M")
    #'''
    if request.method == 'POST' and 'btn_form_zgloszenie' in request.POST:

        if form_podjecie_zgloszenia.is_valid():
            autor = get_author(request.user)
            form_podjecie_zgloszenia.instance.serwisant = autor
            form_podjecie_zgloszenia.instance.data_otwarcia = request.POST.get('data_otwarcia')
            form_podjecie_zgloszenia.instance.czas_otwarcia = request.POST.get('czas_otwarcia')
            form_podjecie_zgloszenia.instance.status = status
            print(
                'autor:', autor,
                ' ; autor.id:', autor.id,
                ' ; data_otwarcia:', data_otwarcia,
                ' ; czas_otwarcia:', czas_otwarcia,
                ' ; status:', status)
            form_podjecie_zgloszenia.save()
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
                ' ; data_wpisu:', data_otwarcia,
                ' ; czas_wpisu:', czas_otwarcia,
                ' ; tresc:', tresci,
                ' ; zgloszenie:', zgloszenie_com)
            form_komentarze.save()
    #'''

    context = {
        'zgloszenia': zgloszenia,
        'form_podjecie_zgloszenia': form_podjecie_zgloszenia,
        'data_otwarcia': data_otwarcia,
        'czas_otwarcia': czas_otwarcia,
        'wyslij': wyslij,
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
        return redirect(nowe_zgloszenie)

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
    return redirect(nowe_zgloszenie)


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