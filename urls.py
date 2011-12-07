from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^upload/', 'data_server.views.upload'),
)
