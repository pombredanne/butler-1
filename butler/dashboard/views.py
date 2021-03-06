from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import View
from dashboard.models import Dashboard


class DashboardDetail(View):

    def get(self, request, dashboard_id):
        dashboard = get_object_or_404(Dashboard, pk=dashboard_id)

        ctx = {
            'dashboard': dashboard,
            'last_update': timezone.now()
        }

        if request.is_ajax():
            template_name = 'dashboard/panels.html'
        else:
            template_name = 'dashboard/dashboard_detail.html'

        return render(request, template_name, ctx)


class DashboardList(View):

    def get(self, request):

        dashboards = Dashboard.objects.all().order_by('name')

        ctx = {
            'dashboards': dashboards,
            'last_update': timezone.now()
        }

        if request.is_ajax():
            template_name = 'dashboard/dashboards.html'
        else:
            template_name = 'dashboard/dashboard_list.html'

        return render(request, template_name, ctx)