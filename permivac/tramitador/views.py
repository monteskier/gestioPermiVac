from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Tramit
from .forms import TramitSolForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


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
