from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name=models.CharField(max_length=10)
    exchange=models.CharField(max_length=10)
    sector=models.CharField(max_length=10)
    currency=models.CharField(max_length=10)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StockPrice(models.Model):
    stock=models.ForeignKey(Stock, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    open_price=models.DecimalField(decimal_places=2, max_digits=10)
    close_price=models.DecimalField(decimal_places=2, max_digits=10)
    high_price=models.DecimalField(decimal_places=2, max_digits=10)
    low_price=models.DecimalField(decimal_places=2, max_digits=10)
    volume=models.IntegerField(default=0)

    def __str__(self):
        return self.stock.symbol


class StockHistory(models.Model):
    stock=models.ForeignKey(Stock, on_delete=models.CASCADE)
    market_cap=models.DecimalField(decimal_places=2, max_digits=10)
    pe_ratio=models.DecimalField(decimal_places=2, max_digits=10)
    dividend_yield=models.DecimalField(decimal_places=2,max_digits=10)
    last_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stock.symbol
