from rest_framework import serializers
from .models import Wallets, Transactions

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallets
        fields = ['user','balance','currency','updated_at']

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['id','type','amount','status','stock','quantity','price_per_unit','remarks','updated_at']

class DepositSerializer(serializers.ModelSerializer):
    amount=serializers.DecimalField(decimal_places=2,max_digits=10)
    method=serializers.CharField(max_length=20,required=False)
    reference_id=serializers.CharField(max_length=20, required=False)

class WithdrawSerializer(serializers.ModelSerializer):
    amount=serializers.DecimalField(decimal_places=2,max_digits=10)
    destination=serializers.CharField(max_length=100)
    note=serializers.CharField(required=False)