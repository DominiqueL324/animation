from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rdv.models import  Responsable,Service
from rdv.serializers import Serviceserializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime, random, string

 

class ServiceApi(APIView):
    #serializer_class = RendezVousserializer
    #queryset = RendezVous.objects.all()
    #lookup_field = 'id'
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        service = Service.objects.all()
        serializer = Serviceserializer(service,many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        service = Service.objects.create(
            nom = data['nom'],
            responsable = Responsable.objects.filter(pk=int(data['responsable'])).first()
        )
        service = Service.objects.all()
        serializer = Serviceserializer(service,many=True)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class ServiceDetailsApi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self,id):
        try:
            return Service.objects.filter(pk=id)
        except Service.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        service = self.get_object(id)
        serializer = Serviceserializer(service,many=True)
        return Response(serializer.data)

    def put(self,request,id):
        service  = self.get_object(id)
        data = request.data
        if service.exists():
            service = service.first()
            service.nom = data['nom']
            service.responsable = Responsable.objects.filter(pk=int(data['responsable'])).first()
            service.save()
            service = Service.objects.all()
            serializer = Serviceserializer(service,many=True)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response("bad", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        service = self.get_object(id)
        service.delete()
        service = Service.objects.all()
        serializer = Serviceserializer(service,many=True)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)







