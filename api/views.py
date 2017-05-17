from rest_framework import viewsets, permissions
from api.serializer import *
from api.permissions import *
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class ParkViewSet(viewsets.ModelViewSet):

    queryset = Parking.objects.all()
    serializer_class = ParkSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('etage', 'numero')


class CarViewSet(viewsets.ModelViewSet):

    #queryset = Voiture.objects.all().order_by('immat')
    #serializer_class = CarSerializer
    #permission_classes = (permissions.IsAdminUser,)
    permission_classes = (IsStaffOrReadOnlyForAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Voiture.objects.all().order_by('proprietaire')
        else:
            return Voiture.objects.all().order_by('marque')

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return OwnerSerializer
        else:
            return CarSerializer


class OwnerViewSet(viewsets.ModelViewSet):

    queryset = Voiture.objects.all().order_by('proprietaire')
    serializer_class = OwnerSerializer
    permission_classes = (permissions.IsAdminUser,)
