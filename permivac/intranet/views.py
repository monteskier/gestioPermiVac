from django.shortcuts import render
from tramitador.models import Treballadors
from .models import Links

# Create your views here.
def index(request):
    links_publics = Links.objects.all().filter(tipus='public')
    if request.user is not None:
        links_privats = Links.objects.all().filter(areas__in = request.user.areas.all()).exclude(tipus='public')
        context =  {'links_publics':links_publics, 'links_privats':links_privats}
    else:
        context = {'links_publics':links_publics}
    return render(request, 'index.html',context)
