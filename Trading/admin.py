# Register your models here.
from django.contrib import admin
from .models import Trader,Holding

# Register your models here.
@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    list_display = ('user','stock','transaction','trade_type','quantity','price_per_unit','total_amount','executed_date')

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('user','stock','quantity','average_price','updated_at')
