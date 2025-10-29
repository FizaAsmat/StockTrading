from django.db import models
from rest_framework.authtoken.admin import User


# Create your models here.
class Wallets(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField()
    Currency = models.CharField(max_length=10)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class TransactionType(models.TextChoices):
    BUY = 'Buy','buy'
    SELL = 'Sell','sell'
    DEPOSIT = 'Deposit','deposit'
    WITHDRAW = 'Withdraw','withdraw'


class TransactionStatus(models.TextChoices):
    PENDING = 'Pending','Pending'
    COMPLETED = 'Completed','Completed'
    FAILED = 'Failed','Failed'


class Transactions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    amount = models.FloatField()
    remarks = models.TextField()
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.wallet.user.username

