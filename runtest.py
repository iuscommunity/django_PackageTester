#!/usr/bin/env python
from django.core.management import setup_environ
import settings
setup_environ(settings)

from RepoParser.RepoParser import Parser
from urllib2 import urlopen
from re import compile
from lib.Mock import Mock
from lib.Logger import get_logger
from package_tester.models import Build, Package, Release, Arch
from sys import exit

repo = 'testing'
DL = 'https://dl.iuscommunity.org/pub/ius/%s/CentOS' % (repo)
LOGGER = get_logger()
MOCK = Mock()

def getReleases():
    LOGGER.info('Getting releases from %s' % DL)
    res = urlopen(DL).read()
    releases = compile('<a href="(\d+)/">\d+/</a>').findall(res)
    return releases

def getArchitectures(release):
    DLRELEASE = '%s/%s' % (DL, release)
    LOGGER.info('Getting architectures from %s' % DLRELEASE)
    res = urlopen(DLRELEASE).read()
    architectures = compile('<a href="(.+?)/">.+?/</a>.+-').findall(res)
    architectures.remove('SRPMS')
    return architectures

def getParser(release, arch):
    file = '%s/%s/%s/repodata/primary.xml.gz' % (DL, release, arch)
    LOGGER.info('Reading XML File: %s' % file)
    parser = Parser(url=file)
    return parser

def main():
    failcount = 0
    for release in getReleases():
        LOGGER.info('Working on release %s' % release)
        for arch in getArchitectures(release):
            LOGGER.info('Working on arch %s' % arch)
            LOGGER.info('Scrub %s %s, please wait...' % (release, arch))
            MOCK.scrub(repo, release, arch)
            parser = getParser(release, arch)
            for item in parser.getList():
                name = item['name'][0]
                ver = item['version'][1]['ver']
                rel = item['version'][1]['rel']

                full_package = '%s-%s-%s' % (name, ver, rel)
                LOGGER.info('Installing package: %s' % full_package)
                returncode, output = MOCK.install(repo, release, arch, full_package)
                if returncode != 0:
                    failcount += 1
                LOGGER.info('Mock returned status %s' % returncode)

                build_object, created = Build.objects.get_or_create(label=name)
                release_object, created = Release.objects.get_or_create(label=release)
                arch_object, created = Arch.objects.get_or_create(label=arch)
                package = Package.objects.create(label=full_package, build=build_object, arch=arch_object,
                                          release=release_object, status=returncode, log=output[1])

                LOGGER.info('Updating Database')

    if failcount > 0:
        LOGGER.error('%s package(s) failed to install.', failcount)
        exit(1)
    else:
        LOGGER.info('All packages installed successfully.')

if __name__ == "__main__":
    main()
