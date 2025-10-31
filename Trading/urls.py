from django.urls import path
from .views import BuyStockView, SellStockView, HoldingView

holding_list = HoldingView.as_view({'get': 'list'})
holding_detail = HoldingView.as_view({'get': 'retrieve'})

urlpatterns = [
    path('buy/', BuyStockView.as_view(), name='buy-stock'),
    path('sell/', SellStockView.as_view(), name='sell-stock'),
    path('holdings/', holding_list, name='holding-list'),
    path('holdings/<int:pk>/', holding_detail, name='holding-detail'),
]
