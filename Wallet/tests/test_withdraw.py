import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from users.models import Users
from Wallet.models import Wallets
from rest_framework.test import APITestCase, APIClient


@pytest.mark.django_db
def test_withdraw():
    client = APIClient()
    user = User.objects.create_user(username='testy', password='ab123')
    user_obj=Users.objects.get(user=user)

    wallet = Wallets.objects.create(user=user, balance=Decimal('1000.00'))
    client.force_authenticate(user=user)

    response=client.post('/wallet/withdraw/',{'amount':230},format='json')

    assert response.status_code in [200,201]
    wallet.refresh_from_db()
    assert wallet.balance == Decimal('770.00')
    assert 'transaction_id' in response.data
    assert response.data['status']=='Completed'