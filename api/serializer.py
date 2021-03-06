from rest_framework import serializers
from stationnement.models import *
from django.contrib.auth.models import User, Group


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


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'is_active', 'is_staff', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('name', )
