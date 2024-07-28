from rest_framework import serializers

from bagsstore.models import Bag

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","email","password"]

        read_only_fields=["id"]
    

    def create(self, validated_data):
        
        return User.objects.create_user(**validated_data)  

class BagSerializer(serializers.ModelSerializer):

    Bag=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Bag

        fields="__all__"

        read_only_fields=["id","created_date","updated_date","is_active"]

