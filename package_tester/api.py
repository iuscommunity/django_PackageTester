from tastypie.resources import ModelResource
from package_tester.models import Build, Package, Stat
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization

from tastypie import fields
from tastypie.constants import ALL


class BuildResource(ModelResource):
    class Meta:
        queryset = Build.objects.all()
        resource_name = 'build'
        filtering = {
                'label': ALL
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

class PackageResource(ModelResource):
    build = fields.ForeignKey(BuildResource, 'build', full=True)
    class Meta:
        queryset = Package.objects.all()
        resource_name = 'package'
        filtering = {
                'label': ALL
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

class StatResource(ModelResource):
    class Meta:
        queryset = Stat.objects.all()
        resource_name = 'stat'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()