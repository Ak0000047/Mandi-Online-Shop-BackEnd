from django.contrib.auth.models import User

from rest_framework import serializers
from api.models import Category,MandiMenuItem,Order,Review,Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    # id=serializers.CharField(read_only=True)
    class Meta:
        model=Category
        fields='__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    item=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'


class MandhiSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    category=CategorySerializer(read_only=True)
    reviews=ReviewSerializer(read_only=True,many=True)

    
    class Meta:
        model=MandiMenuItem
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    item=MandhiSerializer(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=Cart
        fields=['id','user','item','date']


class OrderSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    item=MandhiSerializer(read_only=True)
    class Meta:
        model=Order
        fields='__all__'
