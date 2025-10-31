# Stocks/urls.py
from django.urls import path
from .views import StockListView, StockDetailView, StockHistoryView

urlpatterns = [
    path('stocks/', StockListView.as_view(), name='stock-list'),
    path('stocks/<str:symbol>/', StockDetailView.as_view(), name='stock-detail'),
    path('stocks/<str:symbol>/history/', StockHistoryView.as_view(), name='stock-history'),
]
