from django.shortcuts import render
from tramitador.models import Treballadors
from django.shortcuts import redirect
from .models import Links

# Create your views here.
def index(request):
    if request.method =='POST':
        pk = request.POST.get('seleccio')
        user = get_object_or_404(Treballadors, pk=pk)
        request.user = user
        auth.login(request, user)

    links_publics = Links.objects.all().filter(tipus='public')
    try:
        if request.user is not None:
            links_privats = Links.objects.all().filter(areas__in = request.user.areas.all()).exclude(tipus='public')
            context =  {'links_publics':links_publics, 'links_privats':links_privats}
        else:
            context = {'links_publics':links_publics}
    except:
        context = {'links_publics':links_publics}
    return render(request, 'index.html',context)

def redireccio(request):
    response = redirect('permivac/intranet/')
    return response
