from .models import Stock, StockPrice, StockHistory
from celery import shared_task
import yfinance as yf
from decimal import Decimal
from datetime import datetime
import random
import logging
logger = logging.getLogger(__name__)


@shared_task(blind=True,autoretry_for=(Exception,),retry_backoff=True)
def ingest_stock_data():
    """
    Periodically injest stock data for US stocks into stock models
    """

    stocks=Stock.objects.filter(is_active=True)

    for stock in stocks:
        try:
            ticker=yf.Ticker(stock.symbol)
            hist=ticker.history(period="1d")

            if hist.empty:
                logger.warning(f"No history for {stock.symbol}")
                continue

            latest=hist.iloc[-1]

            StockPrice.objects.update_or_create(
                stock=stock,
                open_price=Decimal(latest["Open"]),
                high_price=Decimal(latest["High"]),
                low_price=Decimal(latest["Low"]),
                close_price=Decimal(latest["Close"]),
                volume=int(latest["Volume"])
                )

            info=ticker.info
            StockHistory.objects.update_or_create(
                stock=stock,
                defaults={
                    "market_cap":Decimal(info.get("marketCap",0)or 0),
                    "pe_ratio": Decimal(info.get("trailingPE",0)or 0),
                    "dividend":Decimal(info.get("dividend",0)or 0)
                }
            )

            logger.info(f"Updated data for {stock.symbol}")
        except Exception as e:
            logger.error(f" Failed to fetch {stock.symbol}: {e}")
            continue