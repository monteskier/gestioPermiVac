from django.contrib import admin
from .models import Treballadors, Tramit, Document, Area, Calendari
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
"""class TreballadorsAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','dni','email','area','date_joined')"""

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_fieldsets = (
                        (None, {
                            'classes': ('wide',),
                            'fields': ('username','first_name','last_name','dni','email','areas','password1','password2')}
                        ),
                    )
    fieldsets = (
                    (None, {
                    'classes': ('wide',),
                    'fields': ('username','password')}),
                    ('Dades Perosnals',{'fields':('first_name','last_name','email','dni')}),
                    ('Dades sobre el treballador',{'fields':('areas',)}),
                    ('Permissos',{'fields':('is_active','is_staff','is_superuser','groups','representant')}),
                    ('Dades interesants',{'fields':('last_login','date_joined',)}),

                )
    form = CustomUserChangeForm
    model = Treballadors
    list_display =  ['username','first_name','last_name','dni','email','date_joined','representant']

admin.site.register(Treballadors, CustomUserAdmin)

"""Es cra una nova classe per fer la cerca autocompletada dels Tramits"""

class TramitAdmin(admin.ModelAdmin):
    list_display = ('creat_en','get_treballador_nom','get_treballador_cognoms','data_sol','tipus','was_published_recently','finalitzat')
    search_fields = ['treballador__last_name','treballador__first_name',]
    def get_treballador_nom(self, obj):
        return obj.treballador.first_name

    def get_treballador_cognoms(self, obj):
        return obj.treballador.last_name


class DocumentAdmin(admin.ModelAdmin):
    list_display=('descripcio','document')

class CalendariAdmin(admin.ModelAdmin):
    list_display = ('any','get_treballador_nom','get_treballador_cognoms','vacances','perm_precep','perm_no_precep', 'asum_p','asum_p_dies','perm_indisposicio')

    def get_treballador_nom(self, obj):
        return obj.treballador.first_name

    def get_treballador_cognoms(self, obj):
        return obj.treballador.last_name



admin.site.register(Tramit, TramitAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Area)
admin.site.register(Calendari, CalendariAdmin)
