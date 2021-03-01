from django.urls import include, path
from django.conf.urls import url
from django.urls import reverse
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='indexIntranet'),
    url(r'^noticies/',views.noticies, name='noticies'),
    url(r'^nova_noticia/',views.nova_noticia, name='nova_noticia'),
    url(r'^marcatge/',views.marcatge, name='marcatge'),
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
