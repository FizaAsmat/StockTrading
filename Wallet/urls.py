from django.urls import path
from .views import(
    WalletView,
    TransactionsView,
    DepositView,
    WithdrawView
)

urlpatterns = [
    path('',WalletView.as_view(),name='wallet'),
    path('transactions/',TransactionsView.as_view(),name='transactions'),
    path('deposit/',DepositView.as_view(),name='deposit'),
    path('withdraw/',WithdrawView.as_view(),name='withdraw'),
]