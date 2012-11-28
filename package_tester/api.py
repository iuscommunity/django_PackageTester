from tastypie.resources import ModelResource
from package_tester.models import Build, Package, Stat

from tastypie import fields
from tastypie.constants import ALL


class BuildResource(ModelResource):
    class Meta:
        queryset = Build.objects.all()
        resource_name = 'build'
        filtering = {
                'label': ALL
        }

class PackageResource(ModelResource):
    build = fields.ForeignKey(BuildResource, 'build', full=True)
    class Meta:
        queryset = Package.objects.all()
        resource_name = 'package'
        filtering = {
                'label': ALL
        }

class StatResource(ModelResource):
    class Meta:
        queryset = Stat.objects.all()
        resource_name = 'stat'