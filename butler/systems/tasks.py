from urlparse import urljoin
from celery.task import periodic_task, task
from celery.schedules import crontab
import requests
from django.conf import settings
from systems.models import Environment, Machine, Role
from systems.puppetdb import PuppetDB


@periodic_task(run_every=crontab(minute='*/5'))
def sync_nodes():
    url = urljoin(settings.PUPPETDB_URL, 'v3/nodes')
    headers = {
        'Accepts': 'application/json'
    }

    cert = (settings.PUPPETDB_CERT, settings.PUPPETDB_KEY)

    req = requests.get(url, headers=headers, verify=False, cert=cert)

    for node in req.json():
        sync_node(node['name'])


@task
def sync_node(nodename):
    puppetdb = PuppetDB()
    environment_name = puppetdb.get_environment(nodename)
    env, _ = Environment.objects.get_or_create(name=environment_name)
    machine, _ = Machine.objects.get_or_create(environment=env, nodename=nodename)

    roles = []
    for role in puppetdb.get_roles(nodename):
        role, _ = Role.objects.get_or_create(name=role)
        roles.append(role)

    machine.roles = roles
