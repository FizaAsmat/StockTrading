# Stocks/scripts/populate_stocks.py

import random
from decimal import Decimal, ROUND_HALF_UP
from ..models import Stock, StockPrice, StockHistory

def populate_data():
    stocks = [
        {"symbol": "AAPL", "name": "Apple", "exchange": "NASDAQ", "sector": "Tech", "currency": "USD"},
        {"symbol": "GOOGL", "name": "Google", "exchange": "NASDAQ", "sector": "Tech", "currency": "USD"},
        {"symbol": "TSLA", "name": "Tesla", "exchange": "NASDAQ", "sector": "Auto", "currency": "USD"},
        {"symbol": "AMZN", "name": "Amazon", "exchange": "NASDAQ", "sector": "E-commerce", "currency": "USD"},
    ]

    for s in stocks:
        stock, _ = Stock.objects.get_or_create(**s)

        # Generate realistic decimal values
        open_price = Decimal(random.uniform(100, 200)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        close_price = Decimal(random.uniform(100, 200)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        high_price = Decimal(random.uniform(200, 300)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        low_price = Decimal(random.uniform(80, 150)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Create stock price entry
        stock_price = StockPrice.objects.create(
            stock=stock,
            open_price=open_price,
            close_price=close_price,
            high_price=high_price,
            low_price=low_price,
            volume=random.randint(10000, 100000)
        )

        # Update or create stock history
        StockHistory.objects.update_or_create(
            stock=stock,
            defaults={
                "market_cap": Decimal(random.uniform(1_000_000, 2_000_000)).quantize(Decimal('0.01')),
                "pe_ratio": Decimal(random.uniform(10, 40)).quantize(Decimal('0.01')),
                "dividend_yield": Decimal(random.uniform(1, 3)).quantize(Decimal('0.01')),
            }
        )

        # ✅ Update live price for trading (set current_price from close_price)
        stock.current_price = stock_price.close_price
        stock.save(update_fields=['current_price'])
