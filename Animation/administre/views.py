from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from rdv.models import  Administre
from rdv.serializers import  Administreserializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime, random, string
from django.core.mail import send_mail

 

class AdministratreApi(APIView):
    #serializer_class = RendezVousserializer
    #queryset = RendezVous.objects.all()
    #lookup_field = 'id'
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def checkifExist(self,nom):
        user = User.objects.filter(email=nom)
        if user.exists():
            return 0
        else:
            return 0
    
    
    def get(self, request):
        admin = Administre.objects.all()
        serializer = Administreserializer(admin,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        data = request.data
        message =""
        if self.checkifExist(data['email'])== 0:
            user = User()
            user.username = data['email']
            user.first_name = data['prenom']
            user.last_name = data['nom']
            user.email = data['email']
            user.set_password(data['mdp'])
            user.save()
            admin = Administre.objects.create(
                nom=data['nom'],
                prenom=data['prenom'],
                adresse=data['adresse'],
                telephone=data['telephone'],
                email=data['email'],
                user=user,
                password=data['mdp']
            )

            message = "<p>Votre compte administré a été crée avec succès sur la plateforme Animation</p>"
            message = message+"<p>Votre nom d'utilisateur est <strong>"+ admin.email +"</strong></p>"
            message = message+"<p>Votre mot de passe <strong>"+ data['mdp'] +"</strong></p>"
            envoyerMail("Création de compte",message,[data['email']])

        admin = Administre.objects.all()
        serializer = Administreserializer(admin,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        

class AdministreDetailsApi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def checkifExist(self,nom,id):
        user = Administre.objects.filter(email=nom)
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
            return Administre.objects.filter(pk=id)
        except Administre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request,id):
        adm = self.get_object(id)
        serializer = Administreserializer(adm,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id):
        adm  = Administre.objects.filter(pk=id)
        data = request.data
        if self.checkifExist(data['email'],id)== 0:
            adm = adm.first()
            user = adm.user
            user.username = data['email']
            user.first_name = data['prenom']
            user.last_name = data['nom']
            user.email = data['email']
            adm.nom=data['nom']
            adm.prenom=data['prenom']
            adm.adresse=data['adresse']
            adm.telephone=data['telephone']
            adm.email=data['email']
            if data['mdp'] != "":
                adm.password=data['mdp']
                adm.user.set_password(data['mdp'])
            user.save()
            adm.save()

            message = "<p>Votre compte administré a été modifié avec succès sur la plateforme Animation</p>"
            message = message+"<p>Votre nom d'utilisateur est <strong>"+ data['email'] +"</strong></p>"
            if data['mdp']!="":
                message = message+"<p>Votre nouveau mot de passe est <strong>"+ data['mdp'] +"</strong></p>"
            envoyerMail("Modification de compte",message,[data['email']])

            serializer = Administreserializer(Administre.objects.all(),many=True)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response("bad", status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,id):
        administre = self.get_object(id).first()
        user = administre.user.first()
        administre.delete()
        user.delete()
        administre= Administre.objects.all()
        serializer = Administreserializer(administre,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

def envoyerMail(titre,contenu,destinataire):
    send_mail(
            titre,  #subject
            "", 
            "brunoowona12@gmail.com",#from_mail
            destinataire,  #recipient list []
            fail_silently=False,  #fail_silently
            html_message=contenu
    )