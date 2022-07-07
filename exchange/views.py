from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import ExchangeForm
from .models import Currency, CurrencyWallet, Wallet


def home(request):
    return render(request, 'exchange/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'exchange/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('mainpage')
            except IntegrityError:
                return render(request, 'exchange/signupuser.html', {'form': UserCreationForm(), 'error': 'Такое имя пользователя уже существует. Задайте другое'})
        else:
            return render(request, 'exchange/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})



@login_required
def mainpage(request):
    currency = Currency.objects.all()
    print(request.method)
    if request.method == 'POST':
        from_amount = float(request.POST.get('amount', 0))
        currency_from = int(request.POST.get('currency_from', None))
        currency_to = int(request.POST.get('currency_to', None))
        converted_amount = round(float(currency[currency_from - 1].price / currency[currency_to - 1].price) * float(from_amount), 2)

        wallet = Wallet.objects.get(user_id=request.user.id)
        wallet_from = CurrencyWallet.objects.get(wallet_id=wallet.id, currency_id=currency_from)
        wallet_to = CurrencyWallet.objects.get(wallet_id=wallet.id, currency_id=currency_to)

        wallet_from.amount = float(wallet_from.amount) - from_amount
        wallet_to.amount = float(wallet_to.amount) + converted_amount

        wallet_from.save()
        wallet_to.save()
        return redirect('/current')

    wallet = Wallet.objects.get(user_id=request.user.id)
    wallets = CurrencyWallet.objects.filter(wallet_id=wallet.id)
    return render(request, 'exchange/main_page.html', {'currency': currency, 'wallets': wallets, 'form': ExchangeForm()})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'exchange/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'exchange/loginuser.html', {'form': AuthenticationForm(), 'error': 'Неверные данные '
                                                                                                  'для входа'})
        else:
            login(request, user)
            return redirect('mainpage')
