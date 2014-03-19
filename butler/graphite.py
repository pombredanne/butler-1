import urllib
from django.conf import settings
import requests


class GraphiteLoadError(Exception):
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def __repr__(self):
        return "Could not load data from Graphite: %s\n%s" % (self.status_code, self.content)


def get_latest_value(*targets):
    data = get_data(*targets)
    ret = {}

    for stat_name, values in data.iteritems():

        if len(values) > 0:
            latest_val = values[0][0]
        else:
            latest_val = None

        ret[stat_name] = latest_val

    return ret


def get_graph_url(target):
    render_url = '%s/render/' % settings.GRAPHITE_SERVER

    params = {
        'target': target,
        'from': '-30mins',
        'width': 700,
        'height': 500
    }
    return  '%s?%s' % (render_url, urllib.urlencode(params, doseq=True))


def get_data(*targets):
    render_url = '%s/render/' % settings.GRAPHITE_SERVER

    params = {
        'target': targets,
        'from': '-30mins',
        'format': 'json'
    }
    url = '%s?%s' % (render_url, urllib.urlencode(params, doseq=True))

    response = requests.get(url)
    print url
    if not response.ok:
        raise GraphiteLoadError(response.status_code, response.content)

    data = response.json()
    results = {}

    for target in data:
        sorted_data = sorted(target['datapoints'], key=lambda x: x[1], reverse=True)
        sorted_data = [point for point in sorted_data if point[0] is not None]
        results[target['target']] = sorted_data

    return results
