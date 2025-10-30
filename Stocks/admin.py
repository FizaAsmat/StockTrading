from django.contrib import admin
from .models import Stock,StockHistory,StockPrice

# Register your models here.
@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('stock','market_cap','pe_ratio','dividend_yield','last_updated')

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('stock','timestamp','open_price','high_price','low_price','close_price','volume')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol','name','exchange','sector','currency','is_active')