from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.
from django.contrib.auth.models import AbstractUser

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+2)]

def current_year():
    return datetime.date.today().year

class Area(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

class Treballadors(AbstractUser):

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
    areas = models.ManyToManyField(Area)
    """rol = models.CharField(max_length=20, choices = tip_rols, default = 'treb')
    estat = models.CharField(max_length=10, choices = tip_estats, default = 'alta')"""

    def __str__(self):
        return self.username

class Document(models.Model):
    descripcio = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='%Y/%m/')
    pujat_en = models.DateTimeField(auto_now_add=True)
    pujat_per = models.ForeignKey(Treballadors, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcio

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
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    creat_en = models.DateTimeField(auto_now_add=True)
    modificat_en = models.DateTimeField(auto_now=True)
    data_sol = models.CharField(max_length=250, help_text = "Interval de dates amb guións '-', per dies no consecutios emprar ',' Exemple:01/01/2019 - 05/01/2019, 07/01/2019")
    tipus = models.CharField(max_length=40, choices=tipologia, default='asum_p')
    finalitzat = models.BooleanField(default=False)

    """Validacio de RRHH"""
    valRRHH = models.CharField(max_length=20, choices=validacio, default='espera')

    """Validacio del responsable"""
    valResp =  models.CharField(max_length=20, choices=validacio, default='espera')

    """Validacio del Politic"""
    valPol = models.CharField(max_length=20, choices=validacio, default='espera')

    """En cas de voler explicar el motiu"""
    missatge_usuari = models.CharField(max_length=2000, null = True, blank=True)
    missatge_responsable = models.CharField(max_length=2000, null = True, blank=True)

    """Millores per el admin site"""
    def was_published_recently(self):
        return self.creat_en >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'creat_en'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Publicat recentment?'

    def save(self, *args, **kwargs):
        if(self.valRRHH == "conforme" and self.valResp=="conforme" and self.valPol =="conforme"):
            self.finalitzat = True
        super(Tramit, self).save(*args, **kwargs)

    def __str__(self):
        return self.treballador.usuari

class Calendari(models.Model):
    any = models.IntegerField(('any'),choices=year_choices(), default=current_year())
    vacances = models.IntegerField(default=22, verbose_name="Vacances disponibles")
    perm_precep = models.IntegerField(default=0, verbose_name="Permissos preceptius fets:")
    perm_no_precep = models.IntegerField(default=0, verbose_name="Permissos no preceptius fets:")
    asum_p = models.IntegerField(default=6,verbose_name="Assumptes perosnals disponibles:")
    treballador = models.ForeignKey(Treballadors, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.any)
