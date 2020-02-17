from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm): #Classe per el formulari de nou tramit, sense acces als camps de validacio del Responsable i del politic.
    class Meta:
        model = Noticia
        fields = ('titol','text', 'document','publicat','destacada')
        widgets = {
            'creat_en': forms.HiddenInput(),
            'text':forms.Textarea(attrs={'rows':4, 'cols':150}),
            }
        labels = {
            'titol': ('Títol de la Notícia:'),
            'text': ('Cos de la Notícia:'),
            'document' : ('Pujar document:'),
            'publicat' : ('Vols publicar-la?'),
            'destacada' : ('Vols que surti a la plana principal?:'),
        }
        
