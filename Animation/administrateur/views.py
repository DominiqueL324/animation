from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rdv.models import  Administrateur, Responsable,Service
from rdv.serializers import  Adminstrateurserializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime, random, string

 

class AdministrateurApi(APIView):
    #serializer_class = RendezVousserializer
    #queryset = RendezVous.objects.all()
    #lookup_field = 'id'
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def checkifExist(self,nom):
        user = User.objects.filter(username=nom)
        if user.exists():
            return 0
        else:
            return 0
    
    def checkifExistEmail(self,nom):
        user = User.objects.filter(email=nom)
        if user.exists():
            return 1
        else:
            return 0
    
    def get(self, request):
        user = User.objects.all()
        qs = User.objects.none()
        for us in user:
            if us.administrateur.exists():
                qs |= User.objects.filter(id=us.id)
        serializer = UserSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        data = request.data
        user = User()
        if self.checkifExistEmail(data['email']) == 1:
            return Response("email existant", status=status.HTTP_400_BAD_REQUEST)
        if self.checkifExist(data['login']) == 0:
            user.username = data['login']
            user.first_name = data['prenom']
            user.last_name = data['nom']
            user.email = data['email']
            user.set_password(data['mdp'])
            user.save()
        else:
            return Response("login existant", status=status.HTTP_400_BAD_REQUEST)
        
        administrateur = Administrateur.objects.create(
            user = user,
            adresse = data['adresse'],
            telephone = data['telephone'],
        )
        user = User.objects.all()
        qs = User.objects.none()
        for us in user:
            if us.administrateur.exists():
                qs |= User.objects.filter(pk=us.id)
        serializer = UserSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        

class AdministrateurDetailsApi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def checkifExist(self,nom,id):
        user = User.objects.filter(username=nom)
        if user.exists():
            user = user.first()
            if user.id == id:
                return 0
            else:
                return 1 
        else:
            return 0
    
    def checkifExistEmail(self,nom,id):
        user = User.objects.filter(email=nom,id=id)
        if user.exists():
            user = user.first()
            if user.id == id:
                return 0
            else:
                return 1 
        else:
            return 0

    def get_object(self,id):
        try:
            return User.objects.filter(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        user = self.get_object(id)
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)

    def put(self,request,id):
        user  = self.get_object(id).first()
        data = request.data
        administrateur = user.administrateur
        administrateur = administrateur.first()

        if self.checkifExistEmail(data['email'],user.id) == 1:
            return Response("email existant", status=status.HTTP_400_BAD_REQUEST)

        if self.checkifExist(data['login'],id) == 0:
            user.username = data['login']
            user.first_name = data['prenom']
            user.last_name = data['nom']
            user.email = data['email']
            if data['mdp'] != "":
                user.set_password(data['mdp'])
            user.save()
        else:
            return Response("login existant", status=status.HTTP_400_BAD_REQUEST)

        administrateur.adresse = data['adresse']
        administrateur.telephone = int(data['telephone'])
        administrateur.save()
        user = User.objects.all()
        qs = User.objects.none()
        for us in user:
            if us.administrateur.exists():
                qs |= User.objects.filter(pk=us.id)
        serializer = UserSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,id):
        user = self.get_object(id).first()
        administrateur = user.administrateur.first()
        administrateur.delete()
        user.delete()
        administrateur = User.objects.all()
        administrateur = UserSerializer(administrateur,many=True)
        return Response(administrateur.data,status=status.HTTP_200_OK)







