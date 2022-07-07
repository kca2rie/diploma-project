from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    title = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ManyToManyField(Currency, through='CurrencyWallet')


class CurrencyWallet(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)



