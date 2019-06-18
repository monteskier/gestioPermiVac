"""permivac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from tramitador import views

admin.site.site_header = "RRHH AjSVC Admin"
admin.site.site_title = "RRHH AjSVC Portal"
admin.site.index_title = "Benvingut al tramitador de RRHH AjSVC"
urlpatterns = [
    url(r'^$',views.redireccio),
    url(r'^tramitador/', include('tramitador.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$/accounts/login/',views.redireccio),
]
