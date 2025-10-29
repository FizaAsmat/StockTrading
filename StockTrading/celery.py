from __future__ import unicode_literals, absolute_import
from celery import Celery
import os

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','StockTrading.settings')

app=Celery('stocktrading')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
