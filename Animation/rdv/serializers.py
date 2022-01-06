from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.relations import method_overridden
from .models import Administrateur, Evenement, Responsable, RendezVous, ResponsableService,Administre, Service 
from django.contrib.auth.models import User

class Evenementserializer(serializers.ModelSerializer):
    class Meta:
        model= Evenement
        fields = '__all__'

class Serviceserializer(serializers.ModelSerializer):
    class Meta:
        model= Service
        fields = '__all__'

class Responsableserializer(serializers.ModelSerializer):
    class Meta:
        model= Responsable
        fields = '__all__'

class Adminstrateurserializer(serializers.ModelSerializer):
    class Meta:
        model= Administrateur
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    utilisateur = Responsableserializer(read_only=True,many=True)
    administrateur = Adminstrateurserializer(read_only=True,many=True)
    class Meta:
        model = User
        fields = '__all__'

class TrackListingField1(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "evenement":value.intitule+" "+value.lieux,
            "id":value.id
        }
        return result

class TrackListingFieldResponsable(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "nom":value.user.first_name,
            "prenom":value.user.last_name,
            "id":value.id
        }
        return result

class TrackListingFieldAdministre(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "nom":value.nom,
            "prenom":value.prenom,
            "id":value.id
        }
        return result


class RendezVousserializer(serializers.ModelSerializer):
    evenement = TrackListingField1(read_only=True,many=False)
    responsable = TrackListingFieldResponsable(read_only=True,many=False)
    administre = TrackListingFieldAdministre(read_only=True,many=False)
    class Meta:
        model= RendezVous
        fields = '__all__'

class ResponsableServiceserializer(serializers.ModelSerializer):
    class Meta:
        model= ResponsableService
        fields = '__all__'

class TrackListingField(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "date_d":value.date_d,
            "date_f":value.date_f,
            "heure_d":value.heure_d,
            "heure_f":value.heure_f,
            "administre":value.administre.nom+" "+value.administre.prenom,
            "etat":value.etat,
            "responsable":value.responsable.user.first_name+" "+value.responsable.user.last_name,
            "evenement":value.evenement.intitule+" "+value.evenement.lieux,
            "id":value.id

        }
        return result

class Administreserializer(serializers.ModelSerializer):
    rdv=TrackListingField(read_only=True,many=True)
    class Meta:
        model= Administre
        fields = '__all__'
