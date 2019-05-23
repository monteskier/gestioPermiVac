from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Tramit


# Create your views here.

def index(request):
    ultims_tramits = Tramit.objects.order_by('-creat_en')[:5]
    context = {'ultims_tramits':ultims_tramits}
    return render(request, 'tramits/index.html', context)


def detall(request, tramit_id):
    response = "Estas veient el detall del Tramit numero %s."
    return HttpResponse(response % tramit_id)

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
