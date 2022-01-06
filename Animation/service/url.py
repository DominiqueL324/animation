from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import ServiceApi,ServiceDetailsApi
from rest_framework.authtoken import views


urlpatterns = [
    path('viewset/gestion/service/', ServiceApi.as_view()),
    path('viewset/gestion/service/<int:id>', ServiceDetailsApi.as_view()),
]