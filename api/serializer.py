from rest_framework import serializers
from stationnement.models import *


class ParkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Parking
        fields = ('etage', 'numero', 'couvert', 'voiture', 'date_affect')
        # depth = 2 pour voir les attributs de l'objet valeur d'un champ


class CarSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Voiture
        fields = ('marque', 'couleur', 'immat')


class OwnerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Voiture
        fields = ('proprietaire', 'marque', 'couleur', 'immat')
