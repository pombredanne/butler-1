from django.conf.urls import patterns, url
from dashboard.views import DashboardDetail


urlpatterns = patterns('',
       url(r'^(?P<dashboard_id>\d+)$', DashboardDetail.as_view(), name='dashboard_detail'),
)
