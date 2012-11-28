"""
$ coverage run manage.py test package_tester
Creating test database for alias 'default'...
............
----------------------------------------------------------------------
Ran 12 tests in 0.397s

OK
Destroying test database for alias 'default'...

$ coverage report --include=./package_tester/views.py
Name                   Stmts   Miss  Cover
------------------------------------------
package_tester/views      81     14    83%

$ coverage report
Name                                          Stmts   Miss  Cover
-----------------------------------------------------------------
__init__                                          0      0   100%
lib/Mock                                         16     11    31%
lib/__init__                                      0      0   100%
manage                                           11      4    64%
package_tester/__init__                           0      0   100%
package_tester/admin                             21      0   100%
package_tester/api                               31      0   100%
package_tester/backends/__init__                  0      0   100%
package_tester/backends/django_ldap_backend      38     25    34%
package_tester/context/__init__                   0      0   100%
package_tester/context/stat                       7      2    71%
package_tester/decorators/__init__                0      0   100%
package_tester/decorators/auth                   11      3    73%
package_tester/models                            46      3    93%
package_tester/templatetags/__init__              0      0   100%
package_tester/templatetags/tools                55     17    69%
package_tester/tests                             81      0   100%
package_tester/views                             81     14    83%
settings                                         31      0   100%
urls                                             13      0   100%
-----------------------------------------------------------------
TOTAL                                           442     79    82%                                         442    101    77%
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

from package_tester.models import Build, Package, Task, Log

class MyTestCase(TestCase):
    
    def setUp(self):
        # Create initial data
        self.build_label = 'mysql51-5.1.63-1.ius'
        self.build = Build(label=self.build_label)
        self.build.save()
        
        self.task_label = 'mysql51-5.1.63-1.ius.el5.i386'
        self.task = Task(label=self.task_label, release='el5', arch='i386',
                         build = self.build)
        self.task.save()
        
        self.package_label = 'mysql51'
        self.package = Package(label=self.package_label, task=self.task)
        self.package.save()
        
        self.log = Log(status=0, log='Log', package=self.package)
        self.log.save()
        
        self.my_admin = User.objects.create_superuser('admin',
                                                 'admin@test.com', 'password')
        self.client = Client()

    def test_api_usage_view(self):
        response = self.client.get('/api_usage/')
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_build_view(self):
        response = self.client.get('/build/%s/' % self.build_label)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('build' in response.context)
        self.assertTrue('tasks' in response.context)
        self.assertTrue(self.build == response.context['build'])
        self.assertTrue(self.task in response.context['tasks'])
        
    def test_task_view(self):
        response = self.client.get('/task/%s/' % self.task_label)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('task' in response.context)
        self.assertTrue('packages' in response.context)
        self.assertTrue(self.task == response.context['task'])
        self.assertTrue(self.package in response.context['packages'])
        
    def test_package_view(self):
        response = self.client.get('/package/%s/' % self.package.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('package' in response.context)
        self.assertTrue('logs' in response.context)
        self.assertTrue(self.package == response.context['package'])
        self.assertTrue(self.log in response.context['logs'])
    
    def test_package_log_history_view(self):
        response = self.client.get('/package_history/%s/' % self.package.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('package' in response.context)
        self.assertTrue('logs' in response.context)
        self.assertTrue(self.package == response.context['package'])
        self.assertTrue(self.log in response.context['logs'])
        
    def test_package_created_view(self):
        response = self.client.get('/package/%s/%s/' % (self.package.id,
                                                       self.log.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('package' in response.context)
        self.assertTrue('logs' in response.context)
        self.assertTrue(self.package == response.context['package'])
        self.assertTrue(self.log in response.context['logs'])

    def test_mylogin_view_authed(self):
        self.client.login(username='admin', password='password')
        response = self.client.get('/login/')
        self.assertRedirects(response, '/tasks/', 302, 200)
        response = self.client.get('/tasks/')
        self.assertTrue('user' in response.context)
        self.assertTrue('admin' == response.context['user'].username)

    def test_mylogin_view_unauthed(self):
       response = self.client.get('/login/')
       self.assertEqual(response.status_code, 200)
       
    def test_mylogin_view_badauth(self):
       self.client.login(username='admin', password='')
       response = self.client.get('/login/')
       self.assertEqual(response.status_code, 200)
       
    def test_mylogout_view_authed(self):
        self.client.login(username='admin', password='password')
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/tasks/', 302, 200)
        
    def test_mylogout_view_unauthed(self):
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/tasks/', 302, 200)