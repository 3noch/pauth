from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    (r'^/?$', direct_to_template, {'template': 'index.html'}),
    url(r'^confidential/', include('confidential.urls')),
    (r'^static/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': settings.STATIC_PATH}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
