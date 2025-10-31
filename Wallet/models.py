from django.db import models
from django.contrib.auth.models import User
from Stocks.models import Stock

# Create your models here.
class Wallets(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
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


class TransactionQuerySet(models.QuerySet):
    def deposit(self):
        return self.filter(type=TransactionType.DEPOSIT)

    def withdraw(self):
        return self.filter(type=TransactionType.WITHDRAW)

    def trades(self):
        return self.filter(type__in=[TransactionType.BUY,TransactionType.SELL])

    def completed(self):
        return self.filter(status=TransactionStatus.COMPLETED)

    def pending(self):
        return self.filter(status=TransactionStatus.PENDING)


class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

    def deposit(self):
        return self.get_queryset().deposit()

    def withdraw(self):
        return self.get_queryset().withdraw()

    def trades(self):
        return self.get_queryset().trades()

    def completed(self):
        return self.get_queryset().completed()

    def pending(self):
        return self.get_queryset().pending()

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price_per_unit = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    amount = models.FloatField()
    remarks = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TransactionManager()

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount}"

    class Meta:
        ordering = ['-updated_at']
