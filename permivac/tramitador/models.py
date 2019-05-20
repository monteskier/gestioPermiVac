from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Treballadors(models.Model):
    tip_areas = (
        ('SE','Serveis Econòmics'),
        ('ST','Serveis Territorials'),
        ('SP','Serveis Personals'),
        ('SC','Seguretat Ciutadana'),
        ('SI','Serveis Interns'),
        ('SO', 'Serveis Organització'),
    )
    tip_rols = (
        ('treb', 'Treballador'),
        ('resp', 'Responsable'),
        ('pol', 'Politic'),
    )
    usuari = models.CharField(max_length=20)
    nom = models.CharField(max_length=20)
    cognoms = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    dni = models.CharField(max_length=20)

    area = models.CharField(max_length=200,choices = tip_areas, default = 'SO')
    rol = models.CharField(max_length=20, choices = tip_rols, default = 'treb')



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
    datacreacio = models.DateTimeField('date published')
    data_sol = models.CharField(max_length=250)
    tipus = models.CharField(max_length=40, choices=tipologia, default='asum_p')

    """Validacio del responsable"""
    valResp =  models.CharField(max_length=7, choices=validacio, default='espera')

    """Validacio del Politic"""
    valPol = models.CharField(max_length=7, choices=validacio, default='espera')

    """En cas de voler explicar el motiu"""
    missatge_usuari = models.CharField(max_length=250)
    missatge_responsable = models.CharField(max_length=250)
