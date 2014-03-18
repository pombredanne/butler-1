from django.conf.urls import patterns, url
from django.views.generic import ListView
from systems.models import Machine
from systems.views import MachineAjaxUpdate


urlpatterns = patterns('',
   url(r'^$', ListView.as_view(model=Machine), name='machine_list'),
   url(r'^latest$', MachineAjaxUpdate.as_view(), name='machine_list_update')
)
