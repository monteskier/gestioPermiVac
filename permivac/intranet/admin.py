from django.contrib import admin
from .models import Links, Manual, Noticia

class LinksAdmin(admin.ModelAdmin):
    fields = ['titol','url','tipus','areas']
class ManualAdmin(admin.ModelAdmin):
    list_display = ('titol','creat_en','publicat')
    fields = ['titol', 'publicat']
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titol','creat_en','publicat')
    fields = ['titol','text','publicat']
# Register your models here.
admin.site.register(Links,LinksAdmin)
admin.site.register(Manual,ManualAdmin)
admin.site.register(Noticia,NoticiaAdmin)
