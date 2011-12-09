from django.conf.urls.defaults import patterns, url

import views


urlpatterns = patterns('',
    url(r'^/?$', views.get_all_scopes),
    url(r'^(?P<client>[^/]*)/?$', views.get_client_scopes),
)
