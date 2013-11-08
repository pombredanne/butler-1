from urlparse import urljoin
from celery.task import periodic_task
from celery.schedules import crontab
import requests
from django.conf import settings


@periodic_task(run_every=crontab(minute='*/5'))
def sync_nodes():
    url = urljoin(settings.PUPPETDB_URL, 'v3/nodes')
    headers = {
        'Accepts': 'application/json'
    }
    req = requests.get(url, headers=headers)
    print req.json()