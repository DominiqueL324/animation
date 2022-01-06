from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import ResponsableApi,ResponsableDetailsApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/gestion/responsable/', ResponsableApi.as_view()),
    path('viewset/gestion/responsable/<int:id>', ResponsableDetailsApi.as_view()),
]