
from django.contrib import admin
from django.urls import path
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('rdv.url')),
    path('',include('evenement.url')),
    path('',include('service.url')),
    path('',include('responsable.url')),
    path('',include('administrateur.url')),
    path('',include('administre.url')),
]

