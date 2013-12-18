from urlparse import urljoin
from celery.task import periodic_task, task
from celery.schedules import crontab
import requests
from django.conf import settings
from systems.models import Environment, Machine
from systems.puppetdb import PuppetDB


@periodic_task(run_every=crontab(minute='*/5'))
def sync_nodes():
    url = urljoin(settings.PUPPETDB_URL, 'v3/nodes')
    headers = {
        'Accepts': 'application/json'
    }
    req = requests.get(url, headers=headers, verify=False)

    for node in req.json():
        sync_node(node['name'])


@task
def sync_node(nodename):
    puppetdb = PuppetDB()
    environment_name = puppetdb.get_environment(nodename)
    env = Environment.objects.get_or_create(environment_name)
    Machine.objects.get_or_create(environment=env, nodename=nodename)
