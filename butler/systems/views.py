from django.http import HttpResponse
from django.views.generic import View
import json
from systems.models import Machine


class MachineAjaxUpdate(View):

    def get(self, _):
        data = {}
        for machine in Machine.objects.all():
            data[machine.id] = {
                'security': machine.security_packages,
                'total': machine.total_packages,
                'reboot': machine.requires_restart
            }

        return HttpResponse(content=json.dumps(data), content_type='application/json')
