from dashboard.models import Dashboard


def add_dashboard_list(request):
    return {
        'all_dashboards': Dashboard.objects.all()
    }