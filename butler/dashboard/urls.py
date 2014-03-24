from django.conf.urls import patterns, url
from dashboard.views import DashboardDetail, DashboardList


urlpatterns = patterns('',
    url(r'^$', DashboardList.as_view(), name='dashboard_list'),
    url(r'^(?P<dashboard_id>\d+)$', DashboardDetail.as_view(), name='dashboard_detail'),
)
