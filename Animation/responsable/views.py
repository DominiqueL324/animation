from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rdv.models import  Responsable,Service
from rdv.serializers import  Responsableserializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime, random, string

 

class ResponsableApi(APIView):
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
    
    def checkifExistCouleurCo(self,nom):
        user = Responsable.objects.filter(couleur_conge=nom)
        if user.exists():
            return 1
        else:
            return 0
    
    def get(self, request):
        user = User.objects.all()
        #responsable = Responsable.objects.all()
        qs = User.objects.none()
        for us in user:
            if us.utilisateur.exists():
                qs |= User.objects.filter(pk=us.id)
        serializer = UserSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        data = request.data
        user = User()
        if self.checkifExistEmail(data['email']) == 1:
            return Response("email existant", status=status.HTTP_400_BAD_REQUEST)
        if self.checkifExistCouleurCo(data['couleur_jo']) == 1:
            return Response("couleur_jo existant", status=status.HTTP_400_BAD_REQUEST)
        if self.checkifExist(data['login']) == 0:
            user.username = data['login']
            user.first_name = data['prenom']
            user.last_name = data['nom']
            user.email = data['email']
            user.set_password(data['mdp'])
            user.save()
        else:
            return Response("login existant", status=status.HTTP_400_BAD_REQUEST)
        
        responsable = Responsable.objects.create(
            user = user,
            adresse = data['adresse'],
            telephone = data['telephone'],
            couleur_js = data['couleur_js'],
            couleur_conge = data['couleur_jo']
        )
        user = User.objects.all()
        qs = User.objects.none()
        for us in user:
            if us.utilisateur.exists():
                qs |= User.objects.filter(pk=us.id)
        serializer = UserSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        

class ResponsableDetailsApi(APIView):
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
    
    def checkifExistCouleurCo(self,nom,id):
        user = Responsable.objects.filter(couleur_conge=nom,id=id)
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
        responsable = user.utilisateur
        responsable = responsable.first()

        if self.checkifExistEmail(data['email'],user.id) == 1:
            return Response("email existant", status=status.HTTP_400_BAD_REQUEST)
        if self.checkifExistCouleurCo(data['couleur_jo'],responsable.id) == 1:
            return Response("couleur_jo existant", status=status.HTTP_400_BAD_REQUEST)

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

        responsable.adresse = data['adresse']
        responsable.telephone = int(data['telephone'])
        responsable.couleur_js = data['couleur_js']
        responsable.couleur_conge = data['couleur_jo']
        responsable.save()
        user = User.objects.all()
        qs = User.objects.none()
        for us in user:
            if us.utilisateur.exists():
                qs |= User.objects.filter(pk=us.id)
        serializer = UserSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,id):
        user = self.get_object(id).first()
        responsable = user.utilisateur.first()
        responsable.delete()
        user.delete()
        responsable = User.objects.all()
        responsable = UserSerializer(responsable,many=True)
        return Response(responsable.data,status=status.HTTP_200_OK)







