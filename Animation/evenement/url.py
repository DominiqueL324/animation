from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import EvenementApi, EvenementDetailsApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/gestion/evenement/', EvenementApi.as_view()),
    path('viewset/gestion/evenement/<int:id>', EvenementDetailsApi.as_view()),
]