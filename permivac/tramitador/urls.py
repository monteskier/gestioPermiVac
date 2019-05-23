from django.urls import include, path
from django.conf.urls import url
from django.urls import reverse
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tramit_id>[0-9]+)/$',views.detall, name='detall'),
    #new line logins system jma
    path('accounts/', include('django.contrib.auth.urls')),
]
