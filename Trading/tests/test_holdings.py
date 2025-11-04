import pytest
from rest_framework.test import APIClient
from decimal import Decimal
from django.contrib.auth.models import User
from Wallet.models import Wallets
from Stocks.models import Stock
from users.models import Users
from Trading.models import Holding


@pytest.mark.django_db
def test_create_holding():
    client = APIClient()

    user = User.objects.create_user(username='test3', password='123456')
    user_obj = Users.objects.create(user=user)
    wallet = Wallets.objects.create(user=user, balance=Decimal('1000.00'))
    stock = Stock.objects.create(name='Apple', symbol='AAPL', current_price=Decimal('100.00'))

    client.force_authenticate(user=user)
    client.post('/trading/buy/', {'symbol': 'AAPL', 'quantity': 3}, format='json')
    client.post('/trading/sell/', {'symbol': 'AAPL', 'quantity': 1}, format='json')

    holdings = Holding.objects.get(user=user_obj, stock=stock)


    response = client.get('/trading/holdings/')
    assert response.status_code == 200
    holdings.refresh_from_db()
    assert holdings.quantity==2
    assert holdings.average_price==stock.current_price
