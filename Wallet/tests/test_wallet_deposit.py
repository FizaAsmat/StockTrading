import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from users.models import Users
from rest_framework.test import APIClient
from Wallet.models import Wallets

@pytest.mark.django_db
def test_wallet_deposit():
    client = APIClient()

    user=User.objects.create_user(username="user1",password="abcd1")
    user_obj=Users.objects.create(user=user)

    wallet=Wallets.objects.create(user=user,balance=Decimal('900.00'))
    client.force_authenticate(user=user)

    response = client.post('/wallet/deposit/', {'amount': '1000.00'}, format='json')

    assert response.status_code in [200,201]
    wallet.refresh_from_db()
    assert wallet.balance == Decimal('1900.00')
    assert 'transaction_id' in response.data
    assert response.data['status']=='Completed'