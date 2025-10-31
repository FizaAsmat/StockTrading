# Stocks/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
import json
import redis

from .models import Stock, StockPrice, StockHistory
from .serializers import StockSerializer, StockPriceSerializer, StockHistorySerializer


# Connect to Redis (make sure Redis server is running)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# ---------------------------- STOCK LIST VIEW ----------------------------
class StockListView(APIView):
    """
    List all active stocks.
    Cached in Redis for 5 minutes for performance improvement.
    """

    def get(self, request):
        cache_key = "stocks:list"
        cached_data = r.get(cache_key)

        # ✅ If data is already cached, return directly
        if cached_data:
            print("Serving from Redis cache ✅")
            stocks_data = json.loads(cached_data)
            return Response(stocks_data)

        # ✅ Otherwise fetch from DB
        queryset = Stock.objects.filter(is_active=True)
        serializer = StockSerializer(queryset, many=True)

        # ✅ Cache the serialized data for 5 minutes (300 seconds)
        r.setex(cache_key, 300, json.dumps(serializer.data))
        print("Fetched from DB and cached ✅")

        return Response(serializer.data)


# ---------------------------- STOCK DETAIL VIEW ----------------------------
class StockDetailView(APIView):
    """
    Retrieve details of a specific stock by its symbol.
    Cached in Redis for 5 minutes.
    """

    def get(self, request, symbol):
        cache_key = f"stock:{symbol}"
        cached_data = r.get(cache_key)

        if cached_data:
            print(f"Serving {symbol} from cache ✅")
            stock_data = json.loads(cached_data)
            return Response(stock_data)

        stock = get_object_or_404(Stock, symbol=symbol)
        serializer = StockSerializer(stock)

        # Cache stock detail
        r.setex(cache_key, 300, json.dumps(serializer.data))
        print(f"Fetched {symbol} from DB and cached ✅")

        return Response(serializer.data)


# ---------------------------- STOCK HISTORY VIEW ----------------------------
class StockHistoryView(APIView):
    """
    Retrieves recent price history (last 30 entries) of a given stock symbol.
    """

    def get(self, request, symbol):
        cache_key = f"stock:{symbol}:history"
        cached_data = r.get(cache_key)

        if cached_data:
            print(f"Serving {symbol} history from cache ✅")
            return Response(json.loads(cached_data))

        stock = get_object_or_404(Stock, symbol=symbol)
        history = StockPrice.objects.filter(stock=stock).order_by('-created_at')[:30]
        serializer = StockPriceSerializer(history, many=True)

        r.setex(cache_key, 300, json.dumps(serializer.data))
        print(f"Fetched {symbol} history from DB and cached ✅")

        return Response(serializer.data)
