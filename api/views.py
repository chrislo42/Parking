from rest_framework import viewsets, permissions
from api.serializer import *
from api.permissions import *

# Create your views here.


class ParkViewSet(viewsets.ModelViewSet):

    queryset = Parking.objects.all()
    serializer_class = ParkSerializer
    permission_classes = (IsStaffOrReadOnly,)


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
