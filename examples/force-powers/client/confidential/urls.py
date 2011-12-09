from django.conf.urls.defaults import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^authorize/$', views.authorize),
    url(r'^authorize/response/$', views.authorize_response),
    url(r'^authorize/request-access-token/$', views.access_token)
)
