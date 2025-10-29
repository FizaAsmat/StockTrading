from django.db import models
from ..users.models import Users
from rest_framework.authtoken.admin import User

class TradeType(models.TextChoices):
    BUY='Buy','buy'
    SELL='Sell','sell'


# Create your models here.
class Trader(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    transaction = models.OneToOneField()
    trade_type=models.CharField(choices=TradeType.choices, max_length=10)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    total_amount = models.FloatField()
    executed_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Holding(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    average_price = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username