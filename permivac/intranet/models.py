from django.db import models
from tramitador.models import Area

# Create your models here.
class Links(models.Model):
    titol = models.CharField(max_length=100)
    url = models.CharField(max_length=250)
    tipologia = (
        ('privat','privat'),
        ('public','public'),
    )
    tipus = models.CharField(max_length=20, choices=tipologia, default='public')
    areas = models.ManyToManyField(Area)
