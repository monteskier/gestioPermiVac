from django.urls import include, path
from django.conf.urls import url
from django.urls import reverse
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nou_tramit/',views.nou_tramit, name='nou_tramit'),
    path('tramit/<int:pk>/', views.tramit_detall, name='tramit_detall'),
    path('tramit_eliminar/<int:pk>/', views.tramit_eliminar, name='tramit_eliminar'),
    #url(r'^(?P<tramit_id>[0-9]+)/$',views.detall, name='detall'),
    #new line logins system jma
    path('accounts/', include('django.contrib.auth.urls')),
]
