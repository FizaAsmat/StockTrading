from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from django.core.cache import cache
from users.models import Users
from .models import Trader, Holding, TradeType
from Stocks.models import Stock
from Wallet.models import Transactions, Wallets
from .serializers import TradeSerializer, HoldingSerializer

class BuyStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user_obj = Users.objects.get(user=request.user)
        except Users.DoesNotExist:
            return Response({"error": "Custom Users instance not found"}, status=status.HTTP_404_NOT_FOUND)

        symbol = request.data.get('symbol')
        quantity = int(request.data.get('quantity'))

        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

        live_price = Decimal(stock.current_price)
        total_amount = live_price * quantity

        # Wallet uses Django User
        wallet = Wallets.objects.get(user=request.user)
        if wallet.balance < total_amount:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_403_FORBIDDEN)

        wallet.balance -= total_amount
        wallet.save()

        # Create Transaction
        transaction = Transactions.objects.create(
            wallet=wallet,
            user=request.user,
            amount=total_amount,
            type='withdraw',
            status='completed'
        )

        # Create Trade
        trade = Trader.objects.create(
            user=user_obj,
            stock=stock,
            transaction=transaction,
            trade_type=TradeType.BUY,
            quantity=quantity,
            price_per_unit=live_price,
            total_amount=total_amount
        )

        # Update or create Holding
        holding, created = Holding.objects.get_or_create(
            user=user_obj,
            stock=stock,
            defaults={
                'quantity': quantity,
                'average_price': live_price
            }
        )
        if not created:
            # update existing holding
            new_total_value = holding.quantity * holding.average_price + total_amount
            holding.quantity += quantity
            holding.average_price = new_total_value / holding.quantity
            holding.save()

        # Clear cache
        cache.delete(f"user_{user_obj.id}_holdings")

        return Response(TradeSerializer(trade).data, status=status.HTTP_200_OK)


class SellStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_obj = Users.objects.get(user=request.user)
        except Users.DoesNotExist:
            return Response({"error": "Custom Users instance not found"}, status=status.HTTP_404_NOT_FOUND)

        symbol = request.data.get('symbol')
        quantity = int(request.data.get('quantity'))

        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            return Response({"error":"Stock not found"},status=status.HTTP_404_NOT_FOUND)

        try:
            holding = Holding.objects.get(user=user_obj, stock=stock)
        except Holding.DoesNotExist:
            return Response({"error":"Holding not found"},status=status.HTTP_404_NOT_FOUND)

        if holding.quantity < quantity:
            return Response({"error":"Not enough stock to sell"}, status=status.HTTP_403_FORBIDDEN)

        live_price = Decimal(stock.current_price)
        total_amount = live_price * quantity

        # Update wallet
        wallet = Wallets.objects.get(user=request.user)
        wallet.balance += total_amount
        wallet.save()

        # Create transaction
        transaction = Transactions.objects.create(
            wallet=wallet,
            user=request.user,
            amount=total_amount,
            type='deposit',
            status='completed'
        )

        # Create trade
        trade = Trader.objects.create(
            user=user_obj,
            stock=stock,
            transaction=transaction,
            trade_type=TradeType.SELL,
            quantity=quantity,
            price_per_unit=live_price,
            total_amount=total_amount
        )

        # Update holding
        holding.quantity -= quantity
        if holding.quantity == 0:
            holding.delete()
        else:
            holding.save()

        cache.delete(f"user_{user_obj.id}_holdings")

        return Response(TradeSerializer(trade).data, status=status.HTTP_200_OK)


class HoldingView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = Users.objects.get(user=request.user)
        cache_key = f"user_{user_obj.id}_holdings"
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)

        holdings = Holding.objects.filter(user=user_obj)
        serializer = HoldingSerializer(holdings, many=True)
        cache.set(cache_key, serializer.data)
        return Response(serializer.data)
