from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from package_tester.api import BuildResource, PackageResource, StatResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(BuildResource())
v1_api.register(PackageResource())
v1_api.register(StatResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'package_tester.views.home', name='home_view'),
    url(r'^packages/$', 'package_tester.views.packages', name='packages_view'),
    url(r'^builds/$', 'package_tester.views.builds', name='builds_view'),
    url(r'^login/$', 'package_tester.views.mylogin', name='login_view'),
    url(r'^logout/$', 'package_tester.views.mylogout', name='logout_view'),

    url(r'^search/$', 'package_tester.views.search',
        name='search_view'),

    url(r'^package/(?P<package_id>[0-9]+)/$', 'package_tester.views.package',
        name='package_view'),

    url(r'^build/(?P<build_id>[0-9]+)/$', 'package_tester.views.build',
        name='build_view'),

    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
