from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from .serializers import WalletSerializer,WithdrawSerializer,DepositSerializer,TransactionsSerializer
from .models import Wallets,Transactions, TransactionType,TransactionStatus
from django.db import transaction

class WalletView(generics.CreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_object(self):
        wallet=Wallets.objects.get_or_create(user=self.request.user)
        return wallet


class TransactionsView(generics.ListAPIView):
    serializer_class = TransactionsSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_queryset(self):
        return Transactions.objects.filter(user=self.request.user)


class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = (permissions.IsAuthenticated)

    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount=serializer.validated_data['amount']
        wallet,_=Wallets.objects.get_or_create(user=self.request.user)

        with transaction.atomic():
            tx=Transactions.objects.create(
                user=self.request.user,
                wallet=wallet,
                amount=amount,
                type=TransactionType.DEPOSIT,
                status=TransactionStatus.PENDING,
                remarks="Deposit initiated"
            )
        return Response({"transaction_id":tx.id,"status": tx.status}, status=status.HTTP_201_CREATED)


class WithdrawView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = (permissions.IsAuthenticated)

    def post(self, request, *args, **kwargs):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount=serializer.validated_data['amount']
        wallet,_=Wallets.objects.get(user=self.request.user)

        if wallet.balance > amount:
            return Response({'error': 'Not enough funds!'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            tx=Transactions.objects.create(
                user=self.request.user,
                wallet=wallet,
                amount=amount,
                type=TransactionType.WITHDRAW,
                status=TransactionStatus.PENDING,
                remarks="Withdraw initiated"
            )
        return Response({"transaction_id": tx.id, "status": tx.staus}, status=status.HTTP_201_CREATED)
