from django.shortcuts import render
from django.contrib.auth.models import User


from rest_framework.decorators import action
from rest_framework import viewsets,mixins,status
from rest_framework.response import Response
from rest_framework import authentication,permissions

from api.serializers import UserSerializer,CategorySerializer,MandhiSerializer,OrderSerializer,CartSerializer,ReviewSerializer
from api.models import MandiMenuItem,Category,Order,Cart

# Create your views here.


class UserCreationView(viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class CategoryView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

class MandiMenuView(viewsets.ModelViewSet):
    serializer_class=MandhiSerializer
    queryset=MandiMenuItem.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    # def get_queryset(self):
    #     qs=MandiMenuItem.objects.all()
    #     if 'category' in self.request.query_params:
    #         cat=self.request.query_params.get('category')
    #         qs=qs.filter(occasion__name=cat)
    #     return qs     

     
    def list(self,request,*args,**kwargs):
        qs=MandiMenuItem.objects.all()
        if 'category' in request.query_params:
            qs=qs.filter(category=request.query_params.get('category'))
        serializer=MandhiSerializer(qs,many=True)
        return Response(data=serializer.data)

    
    @action(methods=['POST'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        serializer=CartSerializer(data=request.data)
        mandhi_obj=MandiMenuItem.objects.get(id=kwargs.get('pk'))
        user=request.user
        if serializer.is_valid():
            serializer.save(item=mandhi_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

    @action(methods=['DELETE'],detail=True)
    def delete_from_cart(self,request,*args,**kwargs):
        
        


        cart_item = Cart.objects.get(id=kwargs.get('pk'))
    
    # Check if the authenticated user owns the cart item
        if cart_item.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
       
        



    @action(methods=['POST'],detail=True)
    def place_order(self,request,*args,**kwargs):
        serializer=OrderSerializer(data=request.data)
        mandhi_obj=MandiMenuItem.objects.get(id=kwargs.get('pk'))
        user=request.user
        if serializer.is_valid():
            serializer.save(item=mandhi_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

    @action(methods=['POST'],detail=True)    
    def add_review(self,request,*args,**kwargs):
        serializer=ReviewSerializer(data=request.data)
        mandhi_obj=MandiMenuItem.objects.get(id=kwargs.get('pk'))
        user=request.user
        if serializer.is_valid():
            serializer.save(item=mandhi_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

class CartsView(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class=CartSerializer
    queryset=Cart.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


    

class OrderView(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class=OrderSerializer
    queryset=Cart.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)