from django.conf.urls import patterns, url
from django.views.generic import ListView
from systems.models import Machine


urlpatterns = patterns('',
   url(r'^$', ListView.as_view(model=Machine), name='machine_list'),
)
