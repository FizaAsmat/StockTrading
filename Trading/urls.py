from django.urls import path
from .views import BuyStockView, SellStockView, HoldingView

urlpatterns = [
    path('buy/', BuyStockView.as_view(), name='buy-stock'),
    path('sell/', SellStockView.as_view(), name='sell-stock'),
    path('holdings/', HoldingView.as_view(), name='user-holdings'),
]
