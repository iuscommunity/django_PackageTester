from django.db import models
    
class Build(models.Model):
    label = models.CharField(max_length=75, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.label

class Release(models.Model):
    label = models.CharField(max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.label

class Arch(models.Model):
    label = models.CharField(max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.label

class Package(models.Model):
    label = models.CharField(max_length=75)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    log = models.TextField()
    status = models.CharField(max_length=25)
    arch = models.CharField(max_length=10)
    release = models.CharField(max_length=5)
    build = models.ForeignKey(Build)
        
    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        # When ever we ever create a Log object we
        # successfully ran a build
        if self.id is None:
            stat, created = Stat.objects.get_or_create(id=1, label='statistics')
            if created:
                stat.tests_completed = 1
            else:
                stat.tests_completed += 1
            stat.save()
        super(Package, self).save(*args, **kwargs)

class Stat(models.Model):
    label = models.CharField(max_length=75, unique=True)
    tests_completed = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.label