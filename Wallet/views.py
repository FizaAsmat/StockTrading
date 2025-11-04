import logging
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.db import transaction
from django.core.cache import cache
from decimal import Decimal
from .serializers import (
    WalletSerializer,
    WithdrawSerializer,
    DepositSerializer,
    TransactionsSerializer,
)
from .models import Wallets, Transactions, TransactionType, TransactionStatus

# ✅ Set up a logger for this module
logger = logging.getLogger(__name__)


class WalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cache_key = f"wallet_{user.id}"

        # Step 1: Try to fetch wallet from Redis
        wallet = cache.get(cache_key)
        if wallet:
            logger.info(f"Wallet fetched from Redis for user {user.username}")
            return wallet

        # Step 2: If not in cache, get or create wallet in DB
        wallet, created = Wallets.objects.get_or_create(
            user=user, defaults={"balance": 0.0, "currency": "USD"}
        )

        # Cache the wallet object (for 5 minutes)
        cache.set(cache_key, wallet, timeout=60 * 5)

        if created:
            logger.info(f"Wallet created for user {user.username} and cached in Redis.")
        else:
            logger.info(f"Wallet fetched from DB and cached in Redis for user {user.username}.")

        return wallet


class TransactionsView(generics.ListAPIView):
    serializer_class = TransactionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"user_{user.id}_transactions"

        # Step 1: Try fetching transactions from Redis
        transactions = cache.get(cache_key)
        if transactions:
            logger.info(f"Transactions fetched from Redis for user {user.username}")
            return transactions

        # Step 2: Fetch from DB and cache it
        transactions = (
            Transactions.objects.filter(user=user)
            .order_by("-updated_at")[:10]
        )
        cache.set(cache_key, transactions, timeout=60 * 2)
        logger.info(f"Transactions fetched from DB and cached for user {user.username}")

        return transactions


class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        user = request.user

        wallet, _ = Wallets.objects.get_or_create(
            user=user, defaults={"balance": 0.0, "currency": "USD"}
        )

        with transaction.atomic():
            tx = Transactions.objects.create(
                user=user,
                wallet=wallet,
                amount=amount,
                type=TransactionType.DEPOSIT,
                status=TransactionStatus.PENDING,
                remarks="Deposit initiated",
            )

            # Update wallet balance
            wallet.balance += Decimal(amount)
            wallet.save(update_fields=["balance", "updated_at"])
            tx.status = TransactionStatus.COMPLETED
            tx.save(update_fields=["status"])

            # Invalidate related cache
            cache.delete(f"wallet_{user.id}")
            cache.delete(f"user_{user.id}_transactions")

        logger.info(f"Deposit successful for user {user.username}, amount: {amount}")
        return Response(
            {"transaction_id": tx.id, "status": tx.status},
            status=status.HTTP_201_CREATED,
        )


class WithdrawView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        user = request.user

        wallet = Wallets.objects.filter(user=user).first()
        if not wallet:
            logger.warning(f"Withdraw failed: no wallet found for user {user.username}")
            return Response(
                {"error": "Wallet not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ❌ Fixed logic: Should fail if balance < amount
        if wallet.balance < float(amount):
            logger.warning(f"Withdraw failed: insufficient funds for user {user.username}")
            return Response(
                {"error": "Not enough funds!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            tx = Transactions.objects.create(
                user=user,
                wallet=wallet,
                amount=amount,
                type=TransactionType.WITHDRAW,
                status=TransactionStatus.PENDING,
                remarks="Withdraw initiated",
            )

            # Deduct from wallet
            wallet.balance -= Decimal(amount)
            wallet.save(update_fields=["balance", "updated_at"])
            tx.status = TransactionStatus.COMPLETED
            tx.save(update_fields=["status"])

            # Invalidate cache
            cache.delete(f"wallet_{user.id}")
            cache.delete(f"user_{user.id}_transactions")

        logger.info(f"Withdrawal successful for user {user.username}, amount: {amount}")
        return Response(
            {"transaction_id": tx.id, "status": tx.status},
            status=status.HTTP_201_CREATED,
        )
