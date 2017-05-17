from django.db import models
from django.utils import timezone

# Create your models here.


class Voiture(models.Model):
    proprietaire = models.CharField(max_length=200)
    couleur = models.CharField(max_length=200)
    marque = models.CharField(max_length=200)
    immat = models.CharField(max_length=200)

    def __str__(self):
        return self.marque+" "+self.immat


class Parking(models.Model):
    numero = models.IntegerField()
    etage = models.IntegerField()
    couvert = models.BooleanField()
    voiture = models.ForeignKey('Voiture')
    date_affect = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "et : "+str(self.etage)+" num : "+str(self.numero)

