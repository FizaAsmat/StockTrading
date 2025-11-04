from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import BuyStockView, SellStockView, HoldingView

router = DefaultRouter()
router.register(r'holdings', HoldingView, basename='holding')

urlpatterns = [
    path('buy/', BuyStockView.as_view(), name='buy-stock'),
    path('sell/', SellStockView.as_view(), name='sell-stock'),
    path('', include(router.urls)),
]
