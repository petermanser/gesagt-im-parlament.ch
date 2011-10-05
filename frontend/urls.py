from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('apps.front.views',
    url(r'^$', 'home', name='home'),
    url(r'^persons/$', 'persons', name='persons'),
    url(r'^person/(?P<id>\d+)(-.*)?/$', 'tagcloud', name='tagcloud'),
    url(r'^contact/$', 'contact', name='contact'),
)

if settings.DEBUG:                                                              
    urlpatterns += patterns('',
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )
    urlpatterns += patterns('django.views.static',                              
        url(r'static/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
        url(r'media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )                                                                           
