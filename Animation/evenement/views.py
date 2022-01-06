from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rdv.models import  Administre, Evenement, RendezVous, Responsable
from rdv.serializers import Administreserializer, RendezVousserializer, Evenementserializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime, random, string

 

class EvenementApi(APIView):
    #serializer_class = RendezVousserializer
    #queryset = RendezVous.objects.all()
    #lookup_field = 'id'
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        evt = Evenement.objects.all()
        serializer = Evenementserializer(evt,many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        evt = Evenement.objects.create(
            date_d = data['date_d'],
            date_f = data['date_f'],
            heure_r = data['heure_d'],
            heure_f = data['heure_f'],
            lieux = data['lieux'],
            intitule = data['intitule'],
            jours = data['periode'],
            ville = data['ville'],
            validite = data['validite']
        )
        evt = Evenement.objects.all()
        serializer = Evenementserializer(evt,many=True)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class EvenementDetailsApi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self,id):
        try:
            return Evenement.objects.filter(pk=id)
        except Evenement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        evt = self.get_object(id)
        serializer = Evenementserializer(evt,many=True)
        return Response(serializer.data)

    def put(self,request,id):
        evt  = self.get_object(id)
        data = request.data
        if evt.exists():
            evt = evt.first()
            evt.date_d = data['date_d']
            evt.date_f = data['date_f']
            evt.heure_r = data['heure_d']
            evt.heure_f = data['heure_f']
            evt.lieux = data['lieux']
            evt.jours = data['periode']
            evt.intitule = data['intitule']
            evt.ville = data['ville']
            evt.validite = data['validite']
            evt.save()
            evt = Evenement.objects.all()
            serializer = Evenementserializer(evt,many=True)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response("bad", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        evt = self.get_object(id)
        evt.delete()
        evt = Evenement.objects.all()
        serializer = Evenementserializer(evt,many=True)
        return Response(status=status.HTTP_204_NO_CONTENT)







