from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

from django.contrib.auth.views import login, logout
from testapp.views import main_page_info, requests_log, edit_my_info,\
            remove_log_object

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main_page_info, name='home'),
    url(r'^requests/$', requests_log, name='reqslog'),
    url(r'^remove/$', remove_log_object, name='remove_request'),
    url(r'^editinfo/$', edit_my_info, name='editinfo'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'testingproject.views.home', name='home'),
    # url(r'^testingproject/', include('testingproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
)
