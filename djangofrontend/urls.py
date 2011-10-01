from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Django admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('apps.front.views',
    url(r'^person/(?P<id>\d+)/tagcloud/$', 'tagcloud', name='tagcloud'),
)

if settings.DEBUG:                                                              
    urlpatterns += patterns('django.views.static',                              
        url(r'static/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
        url(r'media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )                                                                           
