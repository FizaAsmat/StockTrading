from rest_framework import serializers
from .models import Trader,TradeType,Holding


class TradeCreateSerializer(serializers.ModelSerializer):
    symbol=serializers.CharField(max_length=100)
    quantity=serializers.DecimalField(decimal_places=2,max_digits=10)

    def validate(self,data):
        symbol=data['symbol']
        quantity=data['quantity']

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields=['id','user','stock','transaction','trade_type','quantity','price_per_unit','total_amount','executed_date']


class HoldingSerializer(serializers.ModelSerializer):
    current_value = serializers.SerializerMethodField()

    def get_current_value(self,obj):
        price= obj.price_per_unit
        if not price:
            return None
        return float(price)*float(obj.quantity)

    class Meta:
        model = Holding
        fields=['stock','average_price','current_value']


class TradeHistorySerializer(serializers.ModelSerializer):
    symbol=serializers.CharField(max_length=100)
    quantity=serializers.DecimalField(decimal_places=2,max_digits=10)

