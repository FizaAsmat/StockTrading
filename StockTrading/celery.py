from __future__ import unicode_literals, absolute_import
from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','StockTrading.settings')

app=Celery('stocktrading')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'fetch_data':{
        'task':'Stocks.tasks.ingest_stock_data',
        'schedule':crontab(minute='*/5'),
    }
}