from django.shortcuts import render
from django.http import HttpResponse
from tramitador.models import Treballadors
from django.shortcuts import redirect
from .models import Links, Noticia, Manual
from .forms import NoticiaForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def getManual():
    manuals = Manual.objects.all().filter(publicat=True)
    context = {'manuals':manuals}
    return context

def getMenu(request):
    links_publics = Links.objects.all().filter(tipus='public')
    try:
        if request.user is not None:
            links_privats = Links.objects.all().filter(areas__in = request.user.areas.all()).exclude(tipus='public')
            context =  {'links_publics':links_publics, 'links_privats':links_privats}
        else:
            context = {'links_publics':links_publics}
    except:
        context = {'links_publics':links_publics}
    return context

def index(request):
    if request.method =='POST':
        pk = request.POST.get('seleccio')
        user = get_object_or_404(Treballadors, pk=pk)
        request.user = user
        auth.login(request, user)
    page = request.GET.get('page', 1)
    noticies = Noticia.objects.all().filter(publicat=True).exclude(destacada=False).order_by('-creat_en')
    paginator = Paginator(noticies, 4)
    try:
        noticies = paginator.page(page)
    except PageNotAnInteger:
        noticies = paginator.page(1)
    except EmptyPage:
        noticies = paginator.page(paginator.num_pages)

    noticies = {'noticies':noticies}
    manual = getManual()
    context = getMenu(request)
    context.update(manual)
    context.update(noticies)

    return render(request, 'index.html',context)


def redireccio(request):
    response = redirect('permivac/intranet/')
    return response

def noticies(request):
    page = request.GET.get('page', 1)
    noticies = Noticia.objects.all().filter(publicat=True).order_by('-creat_en')
    paginator = Paginator(noticies, 4)
    try:
        noticies = paginator.page(page)
    except PageNotAnInteger:
        noticies = paginator.page(1)
    except EmptyPage:
        noticies = paginator.page(paginator.num_pages)


    context = {'noticies':noticies}
    menu = getMenu(request)
    manual = getManual()
    context.update(menu)
    context.update(manual)
    return render(request, 'noticies.html',context)

def nova_noticia(request):
    if request.method =='POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.treballador = request.user
            '''oplinkform = oplinkform(request.POST)'''
            post.save()
            return HttpResponse("Notícia publicada correctament.")
        else:
            return HttpResponse("Dades incorrectes, no s'ha pogut desar")
    else:
        form = NoticiaForm()
        return render(request, 'nova.html',{'form':form})
