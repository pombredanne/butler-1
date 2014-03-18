import requests
import logging
import urllib
from urlparse import urljoin
from celery.task import periodic_task, task
from celery.schedules import crontab
from django.utils import timezone
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
        sync_node.delay(node['name'])


@task
def sync_node(hostname):
    puppetdb = PuppetDB()
    environment_name = puppetdb.get_environment(hostname)
    env, _ = Environment.objects.get_or_create(name=environment_name)

    nodename = hostname.split('.')[0]
    machine, _ = Machine.objects.get_or_create(environment=env, nodename=nodename)

    roles = []
    for role in puppetdb.get_roles(hostname):
        role, _ = Role.objects.get_or_create(name=role)
        roles.append(role)

    machine.roles = roles

    # get the system package information from Graphite
    render_url = 'http://graphite.support.akvo-ops.org/render/'  # TODO: de-hardcode this!
    params = {
        'target': [stat_name % (env.name, machine.nodename) for stat_name in [
            'stats.gauges.systems.%s.%s.packages.security',
            'stats.gauges.systems.%s.%s.packages.total',
            'stats.gauges.systems.%s.%s.requires_restart',
        ]],
        'from': '-30mins',
        'format': 'json'
    }
    url = '%s?%s' % (render_url, urllib.urlencode(params, doseq=True))

    response = requests.get(url)
    if response.ok:
        data = response.json()

        for target in data:
            sorted_data = sorted(target['datapoints'], key=lambda x: x[1], reverse=True)
            if len(sorted_data) > 0:
                latest_val = sorted_data[0][0]
            else:
                latest_val = None

            stat_name = target['target']
            if stat_name.endswith('.packages.security'):
                machine.security_packages = latest_val
            elif stat_name.endswith('.packages.total'):
                machine.total_packages = latest_val
            elif stat_name.endswith('.requires_restart'):
                machine.requires_restart = latest_val is not None and latest_val > 0
            else:
                logging.debug("Unrecognised target: %s" % stat_name)
    else:
        logging.warning("Unable to get system stats for machine %s" % machine)

    machine.last_update = timezone.now()
    machine.save()