from django.contrib import admin
from .models import Currency, Wallet, CurrencyWallet

admin.site.register(Currency)
admin.site.register(Wallet)
admin.site.register(CurrencyWallet)

