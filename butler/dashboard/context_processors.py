from dashboard.models import Dashboard


def add_dashboard_list(_):
    return {
        'all_dashboards': Dashboard.objects.all()
    }