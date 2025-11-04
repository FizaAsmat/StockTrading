import pytest
from rest_framework.test import APIClient
from decimal import Decimal
from django.contrib.auth.models import User
from Wallet.models import Wallets
from Stocks.models import Stock
from users.models import Users

@pytest.mark.django_db
def test_trade_stock_success():
    client = APIClient()

    user = User.objects.create_user(username='test', password='12345')
    user_obj = Users.objects.create(user='user')

    wallet=Wallets.objects.create(user=user, balance=Decimal('1000.00'))
    stock=Stock.objects.create(name='Apple',symbol='AAPL',price=Decimal('100.00'))

    client.force_authenticate(user=user_obj)

    response=client.post('/trading/buy',{'symbol':'AAPL','quantity':1},format='json')

    assert response.status_code == 200
    wallet.refresh_from_db()
    assert wallet.balance == Decimal('900.00')
    assert 'stock_symbol' in response.data
