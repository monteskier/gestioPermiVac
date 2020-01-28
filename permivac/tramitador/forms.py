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
        fields = ('username','first_name','last_name','dni','email','areas','observacions','foto')

class TramitSolForm(forms.ModelForm): #Classe per el formulari de nou tramit, sense acces als camps de validacio del Responsable i del politic.
    class Meta:
        model = Tramit
        fields = ('data_sol','tipus', 'missatge_usuari')
        widgets = {
            'data_sol': forms.HiddenInput(),
            'missatge_usuari':forms.Textarea(attrs={'rows':4, 'cols':150}),
            }
        labels = {
            'data_sol': ('Data/es que es sol·licita/en:'),
            'tipus': ('Tipus de permís:'),
            'missatge_usuari' : ('Missatge optatiu a destacar:'),
        }
        help_text = {
            'data_sol': ("Interval de dates amb guións '-', per dies no consecutios emprar ',' Exemple:01/01/2019 - 05/01/2019, 07/01/2019" ),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
