from django.urls import path

from api import views

from api.serializers import BagSerializer

from rest_framework.viewsets import ModelViewSet

from bagsstore.models import Bag

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()

router.register("bags",views.BagViewSetView,basename="bags")



urlpatterns=[

    path('register/',views.UserCreationView.as_view()),

    path('token/',ObtainAuthToken.as_view()),

]+router.urls