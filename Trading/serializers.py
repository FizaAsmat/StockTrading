from rest_framework import serializers
from .models import Trader,TradeType,Holding
from Stocks.models import Stock
from Wallet.models import Transactions

class TradeSerializer(serializers.ModelSerializer):
    stock_symbol=serializers.CharField(source='stock.symbol',read_only=True)

    class Meta:
        model = Trader
        fields=['id','user','stock','stock_symbol','trade_type','quantity','total_amount','executed_date']


class HoldingSerializer(serializers.ModelSerializer):
    stock_symbol=serializers.CharField(source='stock.symbol',read_only=True)

    class Meta:
        model = Holding
        fields=['id','stock_symbol','quantity','average_price','current_value']