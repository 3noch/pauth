from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^/?$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'index.html'}),

    url(r'^confidential/', include('confidential.urls')),
)

urlpatterns += staticfiles_urlpatterns()
