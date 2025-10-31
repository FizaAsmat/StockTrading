from celery import shared_task
from .scripts.populate_stocks import populate_data
import logging
logger = logging.getLogger(__name__)


@shared_task(bind=True,autoretry_for=(Exception,),retry_backoff=True)
def ingest_stock_data(self):
    """
    Periodically ingest stock data for US stocks into stock models
    """
    logger.info('Ingesting stock data')
    populate_data()
    logger.info('Stock data ingested')
