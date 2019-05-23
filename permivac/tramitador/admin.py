from django.contrib import admin
from .models import Treballadors
from .models import Tramit
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
"""class TreballadorsAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','dni','email','area','date_joined')"""

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Treballadors
    list_display =  ['username','first_name','last_name','dni','email','area','date_joined']

admin.site.register(Treballadors, CustomUserAdmin)

"""admin.site.register(Treballadors, TreballadorsAdmin)"""

class TramitAdmin(admin.ModelAdmin):
    list_display = ('creat_en','get_treballador_nom','get_treballador_cognoms','get_treballador_area','data_sol','tipus','was_published_recently')
    def get_treballador_nom(self, obj):
        return obj.treballador.first_name

    def get_treballador_cognoms(self, obj):
        return obj.treballador.last_name
    def get_treballador_area(self, obj):
        return obj.treballador.area


admin.site.register(Tramit, TramitAdmin)
