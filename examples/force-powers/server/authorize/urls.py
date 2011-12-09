from django.conf.urls.defaults import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.authorize),
    url(r'^response/?$', views.authorize_response)
)
