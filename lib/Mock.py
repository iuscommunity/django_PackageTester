import subprocess

class Mock:

    def __run(self, command):
        'runs a command with the subprocess module'
        process = subprocess.Popen(
            command, shell=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        # wait for our process to complete
        returncode = process.wait()
        message = process.communicate()
        return (returncode, message)

    def scrub(self, repo, release, arch):
        'scrub a new env'
        command = ['/usr/bin/mock', '-r', 'ius-%s-el%s-%s' % (repo, release, arch),
                   '--scrub=all']
        returncode, message = self.__run(command)
        return (returncode, message)

    def __initialize(self, repo, release, arch):
        'init a new mock env'
        command = ['/usr/bin/mock', '-r', 'ius-%s-el%s-%s' % (repo, release, arch),
                   '--init']
        returncode, message = self.__run(command)
        return (returncode, message)

    def install(self, repo, release, arch, package):
        'build a package in our new env'
        self.__initialize(repo, release, arch)
        command = ['/usr/bin/mock', '-r', 'ius-%s-el%s-%s' % (repo, release, arch),
                   '--install', package]
        returncode, message = self.__run(command)
        return (returncode, message)
