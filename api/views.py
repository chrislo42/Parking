from rest_framework import viewsets, filters  # permissions
from api.serializer import *
from api.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
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
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('marque',)

    def get_queryset(self):

        list = self.request.user.groups.values_list('name', flat=True)
        if 'Api_admin'in list:
            return Voiture.objects.all().order_by('proprietaire')
        else:
            return Voiture.objects.all().order_by('marque')

    def get_serializer_class(self):

        list = self.request.user.groups.values_list('name', flat=True)
        if 'Api_admin'in list:
            return OwnerSerializer
        else:
            return CarSerializer


class OwnerViewSet(viewsets.ModelViewSet):

    queryset = Voiture.objects.all().order_by('proprietaire')
    serializer_class = OwnerSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, )
    filter_fields = ('marque',)
    search_fields = ('marque', 'proprietaire', 'immat')
    ordering_fields = ('marque', 'proprietaire')


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAdminUser,)
