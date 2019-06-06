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
def validar(request, pk, rol):
    tramit = get_object_or_404(Tramit, pk=pk)
    print(rol)
    if(("responsables" in rol) and ("RRHH" not in rol)):
        tramit.valResp = "conforme";
        tramit.save();
    elif("RRHH" in rol):
        tramit.valRRHH = "conforme";
        tramit.save();
    elif("politics" in rol):
        tramit.valPol = "conforme";
        tramit.save();

    return redirect ('/tramitador/assignades')

@login_required
def denegar(request, pk, rol):
    tramit = get_object_or_404(Tramit, pk=pk)
    if(("responsables" in rol) and ("RRHH" not in rol)):
        tramit.valResp = "inconforme";
        tramit.save();
    elif("RRHH" in rol):
        tramit.valRRHH = "inconforme";
        tramit.save();
    elif("politics" in rol):
        tramit.valPol = "inconforme";
        tramit.save();

    return redirect ('/tramitador/assignades')


@login_required
def assignades(request):
    groups = request.user.groups.all()
    rol = []
    l = []
    tramits_pendents_RRHH = None
    for g in groups:
        l.append(g.name)

    if "responsables" in l:
        tramits_pendents = Tramit.objects.all().filter(treballador__areas__in = request.user.areas.all()).filter( Q(valResp = "espera") | Q(valRRHH="inconforme")).exclude(finalitzat = True)
        if "RRHH" in l:
            tramits_pendents_RRHH = Tramit.objects.all().filter(~Q(valResp ="espera")).exclude(finalitzat = True)
            rol.append("RRHH")
        rol.append("responsables")


    elif "RRHH" in l:
        tramits_pendents_RRHH = Tramit.objects.all().filter(~Q(valResp ="espera")).exclude(finalitzat = True)
        rol.append("RRHH")

    elif "politics" in l:
        tramits_pendents = Tramit.objects.all().filter(Q(valRRHH = "conforme") & Q(finalitzat = False))
        rol.append('politics')

    if(tramits_pendents_RRHH != None):
        context = {'tramits_pendents': tramits_pendents,'rol': rol, 'tramits_pendents_RRHH':tramits_pendents_RRHH }
        return render(request, 'tramits/assignades.html', context)
    else:
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
def historic(request):
    groups = request.user.groups.all()
    tramits_finalitzats = Tramit.objects.all().filter(Q(treballador__id=request.user.id) & Q(finalitzat=True))
    context = {'tramits_finalitzats': tramits_finalitzats}
    return render(request, 'tramits/historic.html', context)



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
