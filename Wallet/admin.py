from django.contrib import admin
from .models import Wallets, Transactions


# Register your models here.
@admin.register(Wallets)
class WalletsAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'currency', 'updated_at')


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet', 'stock','type', 'quantity', 'price_per_unit', 'status','remarks','updated_at')
