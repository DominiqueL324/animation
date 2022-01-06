from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import  Administre, Evenement, RendezVous, Responsable
from .serializers import Administreserializer, RendezVousserializer, Evenementserializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime, random, string
from django.contrib.auth.models import User
from django.core.mail import send_mail
 

class RdvApi(APIView):
    #serializer_class = RendezVousserializer
    #queryset = RendezVous.objects.all()
    #lookup_field = 'id'
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        rdv = RendezVous.objects.all()
        serializer = RendezVousserializer(rdv,many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        texte = False
        admin = Administre.objects.filter(email=data['email'])
        code = "".join([random.choice(string.ascii_letters) for _ in range(5)])
        mdp = "".join([random.choice(string.ascii_letters) for _ in range(10)]) 
        if not admin.exists():
            texte = True
            user = User()
            user.username = data['email']
            user.first_name = data['prenom']
            user.last_name = data['nom']
            user.email = data['email']
            user.set_password(mdp)
            user.save()
            admin = Administre.objects.create(
                nom=data['nom'],
                prenom=data['prenom'],
                adresse=data['adresse'],
                telephone=data['telephone'],
                email=data['email'],
                user=user,
                password=mdp
            )
        else:
            admin = admin.first()
        rdv = RendezVous.objects.create(
            date_d = data['date_d'],
            date_f = data['date_f'],
            heure_d = data['heure_d'],
            heure_f = data['heure_f'],
            administre = admin,
            etat = "En attente",
            responsable = Responsable.objects.filter(pk=int(data['responsable'])).first(),
            evenement = Evenement.objects.filter(pk=int(data['evenement'])).first(),
            code=code
        )
        dte = rdv.date_d.split("-")
        db = rdv.heure_d.split(":")
        fin = rdv.heure_f.split(":")
        message = ""
        if texte == False:
            message = "<p>Votre rendez-vous pour l'événement <strong>"+rdv.evenement.intitule+"</strong> qui a lieu à/au <strong>"+rdv.evenement.lieux+"</strong>"
            message = message+" a été enregistré avec succès</p><p>il aura lieux le <strong>"+str(dte[2]).zfill(2) + '/' +str(dte[1]).zfill(2) + '/' +str(dte[0])
            message = message+"</strong> à partir de <strong>"+str(db[0]).zfill(2) + ':' +str(db[1]).zfill(2)+"</strong></p>"
            message = message+"<p>Votre code d'achat pour ce rendez-vous est <strong>"+ code +"</strong></p>"
        else:
            message = "<p>Votre rendez-vous pour l'événement <strong>"+rdv.evenement.intitule+"</strong> qui a lieu à/au <strong>"+rdv.evenement.lieux+"</strong>"
            message = message+" a été enregistré avec succès</p><p>il aura lieux le <strong>"+str(dte[2]).zfill(2) + '/' +str(dte[1]).zfill(2) + '/' +str(dte[0])
            message = message+"</strong> à partir de <strong>"+str(db[0]).zfill(2) + ':' +str(db[1]).zfill(2)+"</strong></p>"
            message = message+"<p>Votre code d'achat pour ce rendez-vous est <strong>"+ code +"</strong></p>"
            message = message+"<p>Votre nom d'utilisateur est <strong>"+ admin.email +"</strong></p>"
            message = message+"<p>Votre mot de passe <strong>"+ mdp +"</strong></p>"
        
        envoyerMail("Nouveau Rendez-vous",message,[rdv.administre.email])
        rdv = RendezVous.objects.all()
        serializer = RendezVousserializer(rdv,many=True)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class RdvDetailsApi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self,id):
        try:
            return RendezVous.objects.filter(pk=id)
        except RendezVous.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        rdv = self.get_object(id)
        serializer = RendezVousserializer(rdv,many=True)
        return Response(serializer.data)

    def put(self,request,id):
        rdv  = self.get_object(id)
        data = request.data
        if rdv.exists():
            rdv = rdv.first()
            rdv.date_d = data['date_d']
            rdv.date_f = data['date_f']
            rdv.heure_d = data['heure_d']
            rdv.heure_f = data['heure_f']
            rdv.evenement = Evenement.objects.filter(pk=int(data['evenement'])).first()
            rdv.save()
            dte = rdv.date_d.split("-")
            db = rdv.heure_d.split(":")
            fin = rdv.heure_f.split(":")
            message = "<p>Votre rendez-vous pour l'événement <strong>"+rdv.evenement.intitule+"</strong> qui a lieu à/au <strong>"+rdv.evenement.lieux+"</strong>"
            message = message+" a été mis à jour</p><p>la nouvelle date est de <strong>"+str(dte[2]).zfill(2) + '/' +str(dte[1]).zfill(2) + '/' +str(dte[0])
            message = message+"</strong> à partir de <strong>"+str(db[0]).zfill(2) + ':' +str(db[1]).zfill(2)+"</strong></p>"
            envoyerMail("Modification de Rendez-vous",message,[rdv.administre.email])
            rdv = RendezVous.objects.all()
            serializer = RendezVousserializer(rdv,many=True)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response("bad", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        rdv = self.get_object(id)
        rdv.delete()
        rdv = RendezVous.objects.all()
        serializer = RendezVousserializer(rdv,many=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdministreDetailsApi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        us = User.objects.filter(pk=id).first()
        adm = Administre.objects.filter(pk=us.administre.id)
        serializer = Administreserializer(adm,many=True)
        return Response(serializer.data)

    def put(self,request,id):
        us = User.objects.filter(pk=id).first()
        adm  = Administre.objects.filter(pk=us.administre.id)
        data = request.data
        mdp = request.POST.get('mdp',None)
        if adm.exists():
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
            if mdp != None:
                adm.password=mdp
                adm.user.set_password(mdp)
            user.save()
            adm.save()
            serializer = Administreserializer(Administre.objects.filter(pk=id),many=True)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response("bad", status=status.HTTP_400_BAD_REQUEST)

class EvenementAPi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        evt = Evenement.objects.all()
        serializer = Evenementserializer(evt,many=True)
        return Response(serializer.data)

class RdvByUserApi(APIView):
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        us = User.objects.filter(pk=id).first()
        admin = Administre.objects.filter(pk=us.administre.id)
        rdv = RendezVous.objects.filter(administre=admin.first().id)
        serializer = RendezVousserializer(rdv,many=True)
        return Response(serializer.data)


class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # simply delete the token to force a login
        Token.objects.filter(key=request.GET.get('token',None)).delete()
        #request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

def envoyerMail(titre,contenu,destinataire):
    send_mail(
            titre,  #subject
            "", 
            "brunoowona12@gmail.com",#from_mail
            destinataire,  #recipient list []
            fail_silently=False,  #fail_silently
            html_message=contenu
    )






