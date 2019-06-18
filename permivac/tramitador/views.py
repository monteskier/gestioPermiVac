from django.shortcuts import render, get_object_or_404
from .Calendari import Cal
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Tramit, Document, Treballadors, Calendari
from .forms import TramitSolForm, DocumentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os, datetime
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.forms.models import model_to_dict
# Create your views here.

def redireccio(request):
    response = redirect('permivac/tramitador/')
    return response

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
    return redirect('permivac/tramitador/')


@login_required
def validar(request, pk, rol):
    tramit = get_object_or_404(Tramit, pk=pk)
    print(rol)
    if("responsables" == rol):
        tramit.valResp = "conforme";
        tramit.save();
    elif("RRHH" == rol):
        tramit.valRRHH = "conforme";
        tramit.save();
    elif("politics" == rol):
        tramit.valPol = "conforme";
        tramit.valResp = "conforme";
        tramit.save();
        treballador = tramit.treballador
        if(treballador != None):
            #send_mail('APROVACIO DE LA PETICIO DE DIA O ASSUPMTES PERSONALS',"S'informa de que la seva petició dels dies:"+tramit.data_sol+" ha finalitzat correctament.",'ajsvcsid@gmail.com',[treballador.email,])
            #NOVA LINEA PER RESTAR ELS DIES DEL CALENDARI:
            cal = Cal()
            if(cal.exist(treballador.id)!=False):
                print("Existeix un calendari en aquest treballador")
                dies = cal.recompte(tramit.data_sol)
                cal.gravar(treballador.id,tramit.tipus, dies, tramit.data_sol)

            else:
                print("No existeix cap Calendari de aquest any al treballador")
    return redirect ('/tramitador/assignades')

@login_required
def denegar(request, pk, rol):
    tramit = get_object_or_404(Tramit, pk=pk)
    if(("responsables" in rol) and ("RRHH" not in rol)):
        tramit.valResp = "inconforme"
        tramit.save()
        treballador = tramit.treballador
        if(treballador != None):
            send_mail('DENEGACIÓ DE LA PETICIO DE DIA O ASSUPMTES PERSONALS',"S'informa de que la seva petició dels dies:"+tramit.data_sol+" ha estat rebutjada.\n Posis en contacte amb el Regidor per més informació ",'ajsvcsid@gmail.com',[treballador.email,])

    elif("RRHH" in rol):
        tramit.valRRHH = "inconforme"
        tramit.save()
        treballador = tramit.treballador
        if(treballador != None):
            send_mail('DENEGACIÓ DE LA PETICIO DE DIA O ASSUPMTES PERSONALS',"S'informa de que la seva petició dels dies:"+tramit.data_sol+" ha estat rebutjada.\n Posis en contacte amb el Regidor per més informació ",'ajsvcsid@gmail.com',[treballador.email,])
    elif("politics" in rol):
        tramit.valPol = "inconforme"
        tramit.save()
        treballador = tramit.treballador
        if(treballador != None):
            send_mail('DENEGACIÓ DE LA PETICIO DE DIA O ASSUPMTES PERSONALS',"S'informa de que la seva petició dels dies:"+tramit.data_sol+" ha estat rebutjada.\n Posis en contacte amb el Regidor per més informació ",'ajsvcsid@gmail.com',[treballador.email,])

    return redirect ('permivac/tramitador/assignades')


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
    today = datetime.date.today()
    groups = request.user.groups.all()
    tramits_finalitzats = Tramit.objects.all().filter(Q(treballador__id=request.user.id) & Q(finalitzat=True) &Q(creat_en__year=today.year))
    cal = Cal();
    if(cal.exist(request.user.id)!=False):
        calendari = Calendari.objects.get(treballador__id = request.user.id, any=today.year)
        context = {'tramits_finalitzats': tramits_finalitzats, 'calendari':calendari}
        return render(request, 'tramits/historic.html', context)
    else:
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
            responsables = Treballadors.objects.all().filter(Q(areas__in = request.user.areas.all()) & Q( groups__name = 'responsables'))
            if(responsables != None):
                email = []
                for r in responsables:
                    email.append(r.email)

                send_mail('PETICIO DE DIA O ASSUPMTES PERSONALS', 'El/la treballador/a '+post.treballador.first_name+' i '+post.treballador.last_name+' ha fet una peticio de dies i assumptes a traves d ela plataforma web.\n'+'Sol·licitud:'+post.data_sol+"\n Tipus:"+post.tipus,'ajsvcsid@gmail.com',email)
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
