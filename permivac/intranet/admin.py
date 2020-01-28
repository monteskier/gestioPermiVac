from django.contrib import admin
from .models import Links

class LinksAdmin(admin.ModelAdmin):
    fields = ['titol','url','tipus','areas']
# Register your models here.
admin.site.register(Links,LinksAdmin)
