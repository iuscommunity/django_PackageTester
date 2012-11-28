from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404

import datetime
from package_tester.models import Build, Package
from package_tester.decorators.auth import secure_required

def home(request):
    content = {}
    return render(request, 'home.html', content)

def packages(request):
    content = {}
    packages = Package.objects.filter(created__gte=datetime.date.today())
    content['packages'] = packages
    content['title'] = 'Package Test Ran Today'
    return render(request, 'packages.html', content)

def builds(request):
    content = {}
    builds = Build.objects.all()
    content['builds'] = builds
    return render(request, 'builds.html', content)
    
def package(request, package_id):
    content = {}
    package = Package.objects.get(id=package_id)
    content['package'] = package
    return render(request, 'package.html', content)

def build(request, build_id):
    content = {}
    build = Build.objects.get(id=build_id)
    packages = Package.objects.filter(build=build).order_by('-created')
    content['build'] = build
    content['packages'] = packages
    return render(request, 'build.html', content)

def search(request):
    if request.method == 'GET':
        phrase = request.GET.get('q', '')
        content = {}
        packages = Package.objects.filter(label__icontains=phrase)
        content['packages'] = packages
        content['phrase'] = phrase
        return render(request, 'packages.html', content)

@secure_required
def mylogin(request):
    '''Login a User'''
    if request.user.is_authenticated():
        return redirect(reverse('packages_view'))
        
    if request.method == 'POST':
        auth_form = AuthenticationForm(None, request.POST or None)
        
        # check user is valid and active before letting them in
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return redirect(reverse('packages_view'))

    return render(request, 'login.html')
    
def mylogout(request):
    '''Logout a User'''
    if request.user.is_authenticated():
        logout(request)
    return redirect(reverse('packages_view'))
