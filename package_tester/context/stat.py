from package_tester.models import Stat

def stats(request):
    'The stat object should be available to every page'
    try:
        stat = Stat.objects.get(id=1)
    except Stat.DoesNotExist:
        stat = None
    return { 'stat': stat }