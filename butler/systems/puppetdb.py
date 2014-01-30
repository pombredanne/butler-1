from urlparse import urljoin
from django.conf import settings
import requests


class PuppetDB(object):

    def __init__(self, base_url=settings.PUPPETDB_URL):
        self._base_url = base_url

    def _build_url(self, *parts):
        path = '/'.join(('v3',) + parts)
        return urljoin(self._base_url, path)

    def _get(self, url):
        cert = (settings.PUPPETDB_CERT, settings.PUPPETDB_KEY)
        headers = {
            'Accept': 'application/json'
        }
        req = requests.get(url, headers=headers, verify=False, cert=cert)

        if req.status_code == 200:
            return req.json()
        else:
            print req.content

    def list_nodes(self):
        return self._get(self._build_url('nodes'))

    def get_environment(self, node):
        url = self._build_url('nodes', node, 'facts', 'environment')
        return self._get(url)[0]['value']

    def get_roles(self, node):
        url = self._build_url('nodes', node, 'facts', 'roles')
        return self._get(url)[0]['value']
