from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import AdministrateurApi,AdministrateurDetailsApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/gestion/administrateur/', AdministrateurApi.as_view()),
    path('viewset/gestion/administrateur/<int:id>', AdministrateurDetailsApi.as_view()),
]