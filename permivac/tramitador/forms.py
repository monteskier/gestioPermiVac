from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Treballadors, Tramit, Document

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Treballadors
        fields = ('username','password')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Treballadors
        fields = ('username','first_name','last_name','dni','email','area',)

class TramitSolForm(forms.ModelForm): #Classe per el formulari de nou tramit, sense acces als camps de validacio del Responsable i del politic.
    class Meta:
        model = Tramit
        fields = ('data_sol','tipus', 'missatge_usuari')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
