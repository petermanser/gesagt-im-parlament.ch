from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from apps.front.views import Persons, Person

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('apps.front.views',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^persons/$', Persons.as_view(), name='persons'),
    url(r'^person/(?P<pk>\d+)(-.*)?/$', Person.as_view(), name='tagcloud'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
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
