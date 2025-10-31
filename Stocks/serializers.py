from .models import Stock,StockPrice,StockHistory
from rest_framework import serializers


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class StockPriceSerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField()

    class Meta:
        model = StockPrice
        fields = '__all__'


class StockHistorySerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField()

    class Meta:
        model = StockHistory
        fields = '__all__'