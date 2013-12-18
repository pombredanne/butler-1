from urlparse import urljoin
from django.conf import settings
import requests


class PuppetDB(object):

    def __init__(self, base_url=settings.PUPPETDB_URL):
        self._base_url = base_url

    def _build_url(self, *parts):
        return urljoin(self._base_url, 'v3', *parts)

    def _get(self, url):
        headers = {
            'Accept': 'application/json'
        }
        req = requests.get(url, headers=headers, verify=False)
        return req.json()

    def list_nodes(self):
        return self._get(self._build_url('nodes'))

    def get_environment(self, node):
        url = self._build_url('nodes', node, 'facts', 'environment')
        return self._get(url)['value']
