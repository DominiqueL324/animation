from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import AdministratreApi,AdministreDetailsApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/gestion/administre/', AdministratreApi.as_view()),
    path('viewset/gestion/administre/<int:id>', AdministreDetailsApi.as_view()),
]