from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Tramit, Document
from .forms import TramitSolForm, DocumentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os, datetime
from django.conf import settings
from django.db.models import Q
# Create your views here.

def index(request):
    tramits_pendents = Tramit.objects.all().filter(treballador__id=request.user.id).exclude(finalitzat = True)
    context = {'tramits_pendents': tramits_pendents}
    return render(request, 'tramits/index.html', context)

@login_required
def tramit_detall(request, pk):
    tramit = get_object_or_404(Tramit, pk=pk)
    return render(request, 'tramits/tramit_detall.html', {'tramit': tramit})

@login_required
def tramit_eliminar(request, pk):
    tramit = get_object_or_404(Tramit, pk=pk)
    tramit.delete()
    return redirect('/tramitador/')

@login_required
def assignades(request):
    groups = request.user.groups.all()
    rol = ""
    l = []
    for g in groups:
        l.append(g.name)

    if "responsables" in l:
        tramits_pendents = Tramit.objects.all().filter(treballador__areas__in = request.user.areas.all()).filter( valResp = "espera").exclude(finalitzat = True)
        if "RRHH" in l:
            tramits_pendents = Tramit.objects.all().filter(treballador__areas__in = request.user.areas.all()).filter( Q(valResp = "conforme") | Q(valResp = "espera")).exclude(finalitzat = True)
            rol = "RRHH"
        else:
            tramits_pendents = Tramit.objects.all().filter(treballador__areas__in = request.user.areas.all()).exclude(finalitzat = True)
            rol = "responsables"


    elif "RRHH" in l:
        tramits_pendents = Tramit.objects.all().filter(treballador__areas__in = request.user.areas.all()).filter(valResp = "espera").exclude(finalitzat = True)
        rol = "RRHH"

    elif "politics" in l:
        tramits_pendents = Tramit.objects.all().filter(treballador__areas__in = request.user.areas.all()).filter(valRRHH = "espera").exclude(finalitzat = True)
        rol = 'politics'

    context = {'tramits_pendents': tramits_pendents,'rol': rol}
    return render(request, 'tramits/assignades.html', context)

"""def login(request):
    if(request.method=='POST'):
        usuari = request.POST.get("username");
        contrasenya = request.POST.get("password");
        user = authenticate(username=usuari, password = contrasenya)
        if user is not None and user.is_active:
            auth.login(request, user)
            return render(request, 'tramits/index.html')
        else:
            context = {'response': "Usuari o contrasenyes incorrectes"}
            return render(request, 'tramits/login.html', context)
    else:
        return render(request, 'tramits/login.html')"""

@login_required
def nou_tramit(request):
    if request.method =='POST':
        form = TramitSolForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.treballador = request.user
            post.save()
            return redirect('tramit_detall', pk=post.pk)
        else:
            return HttpResponse("Dades incorrectes, no s'ha pogut desar")
    else:
        form = TramitSolForm()
        #return render(request, 'tramits/tramit_edit.html', {'form':form})
        return render(request, 'tramits/tramit_edit.html',{'form':form})

def upload_document(request):
    if request.method == 'POST' and request.FILES['document'] and request.POST['pk'] != 0:
        pk = int(request.POST['pk'])
        tramit = get_object_or_404(Tramit, pk=pk)

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.tramit = tramit
            post.pujat_per = request.user
            post.descripcio = "DOC_"+tramit.tipus+"_"+str(datetime.datetime.now())
            post.save()
            tramit.document = post
            tramit.save()
            response_data = {}
            response_data['result'] = 'OK'
            response_data['message'] = "Document dessat correctament al Tramit corresponent."
            return JsonResponse(response_data)
        else:
            response_data = {}
            response_data['result'] = 'ERROR'
            response_data['message'] = "Document no s'ha dessat correctament al Tramit corresponent."
            return JsonResponse(response_data)
