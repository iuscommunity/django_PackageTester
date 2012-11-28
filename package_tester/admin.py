from package_tester.models import Build, Package,Stat
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group


admin.site.unregister(Site)
admin.site.unregister(Group)

class BuildAdmin(admin.ModelAdmin):
    list_display = ('label', 'created', 'modified')
admin.site.register(Build, BuildAdmin)

class PackageAdmin(admin.ModelAdmin):
    list_display = ('label', 'build', 'created', 'modified')
admin.site.register(Package, PackageAdmin)

class StatAdmin(admin.ModelAdmin):
    list_display = ('label', 'tests_completed')
admin.site.register(Stat, StatAdmin)