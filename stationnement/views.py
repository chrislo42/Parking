from django.shortcuts import render
from .models import Parking, Voiture
# Create your views here.


def park_list(request):
    parks = Parking.objects.all()
    return render(request, 'stationnement/park_list.html', {'parks': parks})


def car_list(request):
    parks = Parking.objects.all()
    cars = Voiture.objects.all()
    return render(request, 'stationnement/car_list.html', {'cars': cars, 'parks': parks})
