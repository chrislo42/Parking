from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.park_list, name='park_list'),
    url(r'^car/$', views.car_list, name='car_list'),
]
