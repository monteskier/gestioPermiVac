from django.db import models
from tramitador.models import Area
from django.utils import timezone
import datetime

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
    def __str__(self):
        return self.titol

class Noticia(models.Model):
    titol = models.CharField(max_length=100)
    text = models.TextField(null = True, blank=True)
    document = models.FileField(upload_to='noticies', blank=True, null=True)
    creat_en = models.DateTimeField(auto_now_add=True)
    publicat = models.BooleanField(default=False)
    def __str__(self):
        return self.titol

    def was_published_recently(self):
        return self.creat_en >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'creat_en'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Publicat recentment?'


class Manual(models.Model):
    titol = models.CharField(max_length=100)
    text = models.TextField(null = True, blank=True)
    document = models.FileField(upload_to='manuals', blank=True, null=True)
    creat_en = models.DateTimeField(auto_now_add=True)
    publicat = models.BooleanField(default=False)
    def __str__(self):
        return self.titol

    def was_published_recently(self):
        return self.creat_en >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'creat_en'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Publicat recentment?'
