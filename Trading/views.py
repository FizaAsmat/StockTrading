from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from django.core.cache import cache

from .models import Trader, Holding, TradeType
from Stocks.models import Stock
from Wallet.models import Transactions, Wallet
from .serializers import TradeSerializer,HoldingSerializer
# Create your views here.

class BuyStockView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        symbol = request.data.get('symbol')
        quantity = request.data.get('quantity')

        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        live_price = stock.current_price
        total_amount = live_price * quantity

        wallet = Wallet.objects.get(user=user)
        if wallet.balance < total_amount:
            return Response(status=status.HTTP_403_FORBIDDEN)
        wallet.balance -= total_amount
        wallet.save()

        transaction=Transactions.objects.create(
            wallet=wallet,
            amount=total_amount,
            transaction_type='withdraw',
            status='completed'
        )

        trade=Trader.objects.create(
            user=user,
            stock=stock,
            transaction=transaction,
            trade_type='BUY',
            quantity=quantity,
            price_per_unit=live_price,
            total_amount=total_amount
        )
        holding,created=Holding.objects.get_or_create(
            user=user,
            stock=stock,
        )
        if created:
            holding.quantity=quantity,
            holding.average_price=live_price,
        else:
            new_total=holding.quantity * holding.average_price+total_amount,
            holding.quantity+=quantity,
            holding.average_price=new_total/holding.quantity,
        holding.save()

        cache.delete(f"user_{user.id}_holdings")
        return Response(TradeSerializer(trade).data,status=status.HTTP_200_OK)



class SellStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        symbol = request.data.get('symbol')
        quantity = request.data.get('quantity')

        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            return Response({"error":"STock not found"},status=status.HTTP_404_NOT_FOUND)

        try:
            holding=Holding.objects.get(user=user,symbol=symbol)
        except Holding.DoesNotExist:
            return Response({"error":"Holding not found"},status=status.HTTP_404_NOT_FOUND)

        live_price = stock.current_price
        total_amount = live_price*quantity

        wallet = Wallet.objects.get(user=user)
        wallet.balance += total_amount
        wallet.save()

        trasaction=Transactions.objects.create(
            wallet=wallet,
            amount=total_amount,
            transaction_type='deposit',
            status='completed'
        )

        trade=Trader.objects.create(
            user=user,
            stock=stock,
            transaction=trasaction,
            trade_type='Sell',
            quantity=quantity,
            price_per_unit=live_price,
            total_amount=total_amount
        )

        holding.quantity-=quantity,
        if holding.quantity == 0:
            holding.delete()
        else:
            holding.save()

        cache.delete(f"user_{user.id}_holdings")

        return Response(TradeSerializer(trade).data,status=status.HTTP_200_OK)

class HoldingView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        cache_key=user.username+"_Holding"
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)

        holdings = Holding.objects.filter(user=user)
        serializer = HoldingSerializer(holdings, many=True)
        cache.set(cache_key, serializer.data)
        return Response(serializer.data)
