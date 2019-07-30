from django.urls import include, path
from django.conf.urls import url
from django.urls import reverse
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nou_tramit/',views.nou_tramit, name='nou_tramit'),
    url(r'^historic/',views.historic, name='historic'),
    url(r'^calendari/',views.calendari, name='calendari'),
    path('tramit/<int:pk>/', views.tramit_detall, name='tramit_detall'),
    path('tramit_eliminar/<int:pk>/', views.tramit_eliminar, name='tramit_eliminar'),
    path('upload_document/', views.upload_document, name='pujar_document'),
    path('delete_document/', views.delete_document, name='eliminar_document'),
    path('assignades/',views.assignades, name="assignades"),
    path('validar/<int:pk>/<str:rol>', views.validar, name='validar'),
    path('denegar/<int:pk>/<str:rol>', views.denegar, name='denegar'),
    #url(r'^(?P<tramit_id>[0-9]+)/$',views.detall, name='detall'),
    #new line logins system jma
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
