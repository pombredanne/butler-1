from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from dashboard.models import Dashboard


urlpatterns = patterns('',
       url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Dashboard), name='dashboard_detail'),
)
