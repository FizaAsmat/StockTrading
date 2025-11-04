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
    current_value = serializers.SerializerMethodField()

    class Meta:
        model = Holding
        fields=['id','stock_symbol','quantity','average_price','current_value']

    def get_current_value(self, obj):
        """Calculate live value from stock price * quantity"""
        if obj.stock:
            return float(obj.stock.current_price) * obj.quantity
        return 0.0