from django.db import models
from users.models import Users
from Stocks.models import Stock
from Wallet.models import Transactions

class TradeType(models.TextChoices):
    BUY='Buy','buy'
    SELL='Sell','sell'


# Create your models here.
class Trader(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction = models.OneToOneField(Transactions, on_delete=models.CASCADE)
    trade_type=models.CharField(choices=TradeType.choices, max_length=10)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    total_amount = models.FloatField()
    executed_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Holding(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    average_price = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username