from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from qlnhom.models import MonHoc
admin.autodiscover()

dsmon_lookup = {
    'queryset': MonHoc.objects.all(),
    'field': 'ten_mon', # this is the field which is searched
    'field_extract': ['gioi_thieu', 'nam_hoc'],
    #'limit': 10, # default is to limit query to 10 results. Increase this if you like.
    #'login_required': onhocFalse, # default is to allow anonymous queries. Set to True if you want authenticated access.
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GroupManage.views.home', name='home'),
    # url(r'^GroupManage/', include('GroupManage.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('userena.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^$','qlnhom.views.index',name='home_page'),
    (r'^dsmon_lookup/$', 'qlnhom.views.json_lookup', dsmon_lookup),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
