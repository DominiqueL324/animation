from django.db import models
from django.contrib.auth.models import User


class Responsable(models.Model):  
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="utilisateur")
    adresse = models.CharField("Adresse",max_length=300,null=True)
    telephone = models.IntegerField('Téléphone')
    couleur_js = models.CharField("code couleur Jours spécifiques",max_length=60,null=True)
    couleur_conge = models.CharField("code couleur Jours off",max_length=60,null=True)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
        
    class Meta:
        verbose_name = "responsable"

class Evenement(models.Model):
    ville = models.CharField('Ville de l\'évenement',max_length=50,null=True)
    date_d = models.DateField("Date debut evenement")
    date_f = models.DateField("Date fin evenement")
    heure_r = models.TimeField('Heure debut evenement',null=True)
    heure_f = models.TimeField('Heure de fin evenement',null=True)
    lieux = models.CharField('Lieux de evenement',max_length=200)
    intitule = models.CharField('Intitulé de l\'événement',max_length=500,null=True)
    jours = models.CharField('Jour de la semaine', max_length=20,null=True)
    validite = models.CharField("validté de la reservation",max_length=10,null=True)

    def __str__(self):
        return "Evénement à "+self.lieux+" le "
    

class Service(models.Model):
    nom = models.CharField("Nom",max_length=200)
    responsable = models.ForeignKey(Responsable,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "service"


class ResponsableService(models.Model):
    service = models.ForeignKey(Service,on_delete = models.CASCADE)
    responsable = models.ForeignKey(Responsable,on_delete=models.CASCADE)
    def __str__(self):
        return self.service.nom+" --- Responsable: "+self.responsable.user.last_name
        
    class Meta:
        verbose_name = "Responsable de service"

class Administre(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    nom = models.CharField("Nom",max_length=200,null=True)
    prenom = models.CharField("Prenom",max_length=200,null=True)
    email = models.EmailField("Email",max_length=300)
    adresse = models.CharField("Adresse",max_length=300,null=True)
    telephone = models.IntegerField('Téléphone',null=True)
    password = models.CharField("Mot de passe", max_length=300,default="password")

    def __str__(self):
        return self.nom+" "+self.prenom

    class Meta:
        verbose_name = "client"


class Administrateur(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="administrateur")
    adresse = models.CharField("Adresse",max_length=300,null=True)
    telephone = models.IntegerField('Téléphone',null=True)
    password = models.CharField("Mot de passe", max_length=300,default="password")

    def __str__(self):
        return self.nom+" "+self.prenom

    class Meta:
        verbose_name = "administrateur"

class RendezVous(models.Model):
    date_d = models.DateField("Date debut Rdv")
    date_f = models.DateField("Date fin du RDV",null=True)
    heure_d = models.TimeField('Heure debut Rdv',null=True)
    heure_f = models.TimeField('Heure de fin Rdv',null=True)
    code = models.CharField("Code du rendez-vous",max_length=10,null=True)
    administre = models.ForeignKey(Administre,related_name="rdv",on_delete=models.CASCADE)
    etat = models.CharField("Etat du Rdv",max_length=30,default="En attente",null=True)
    responsable = models.ForeignKey(Responsable,on_delete=models.CASCADE,null=True)
    evenement = models.ForeignKey(Evenement,related_name="evenement",on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.client.nom +" "+self.client.prenom +" service: "+self.service.nom 
    
    class Meta:
        verbose_name = "rendez-vous"
        verbose_name_plural = "rendez-vous"

