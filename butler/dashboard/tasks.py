from celery.schedules import crontab
from celery import task
from celery.task import periodic_task
from dashboard.models import Dashboard


@periodic_task(run_every=crontab(minute='*'))
def update_panel_values():
    for dashboard in Dashboard.objects.all():
        for panel in dashboard.panels.all():
            update_panel_value(panel)

@task
def update_panel_value(panel):
    panel.get_value(use_cache=False)