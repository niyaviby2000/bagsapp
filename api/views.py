from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response

from rest_framework.views import APIView

from bagsstore.models import Bag

from django.contrib.auth.models import User

from api.serializers import BagSerializer,UserSerializer

from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication,permissions

class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()


            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
class BagViewSetView(ModelViewSet):

    serializer_class=BagSerializer

    queryset=Bag.objects.all()

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):

        return serializer.save(User=self.request.user)
    
        

    
