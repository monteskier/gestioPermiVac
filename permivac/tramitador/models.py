from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Treballadors(AbstractUser):

    tip_areas = (
        ('SE','Serveis Econòmics'),
        ('ST','Serveis Territorials'),
        ('SP','Serveis Personals'),
        ('SC','Seguretat Ciutadana'),
        ('SI','Serveis Interns'),
        ('SO', 'Serveis Organització'),
    )
    """tip_rols = (
        ('treb', 'Treballador'),
        ('resp', 'Responsable'),
        ('pol', 'Politic'),
    )
    tip_estats = (
        ('alta', 'Alta'),
        ('baixa','Baixa'),
    )
    creat_en = models.DateTimeField(auto_now_add=True)
    modificat_en = models.DateTimeField(auto_now=True)"""
    usuari = models.CharField(max_length=20)
    """nom = models.CharField(max_length=20)
    cognoms = models.CharField(max_length=20)
    email = models.CharField(max_length=50)"""
    dni = models.CharField(max_length=20, null = True, blank=True)
    area = models.CharField(max_length=200,choices = tip_areas, default = 'SO')
    """rol = models.CharField(max_length=20, choices = tip_rols, default = 'treb')
    estat = models.CharField(max_length=10, choices = tip_estats, default = 'alta')"""

    def __str__(self):
        return self.username



class Tramit(models.Model):
    validacio = (
        ('conforme','conforme'),
        ('inconforme','no conforme'),
        ('espera', 'en espera'),
    )
    tipologia = (
        ('vacances', 'Vacances'),
        ('perm_precep', 'Permisos preceptius'),
        ('perm_no_precep', 'Permisos no preceptius'),
        ('asum_p', 'Asumptes personals'),
    )
    treballador = models.ForeignKey(Treballadors, on_delete=models.CASCADE)
    creat_en = models.DateTimeField(auto_now_add=True)
    modificat_en = models.DateTimeField(auto_now=True)
    data_sol = models.CharField(max_length=250)
    tipus = models.CharField(max_length=40, choices=tipologia, default='asum_p')
    finalitzat = models.BooleanField(default=False)

    """Validacio del responsable"""
    valResp =  models.CharField(max_length=7, choices=validacio, default='espera')

    """Validacio del Politic"""
    valPol = models.CharField(max_length=7, choices=validacio, default='espera')

    """En cas de voler explicar el motiu"""
    missatge_usuari = models.CharField(max_length=250, null = True, blank=True)
    missatge_responsable = models.CharField(max_length=250, null = True, blank=True)

    """Millores per el admin site"""
    def was_published_recently(self):
        return self.creat_en >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'creat_en'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Publicat recentment?'


    def __str__(self):
        return self.treballador.usuari
