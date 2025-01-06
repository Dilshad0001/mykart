from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from.models import Product,wishlist,Cart,User
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated



# <---user registration--->

from .serializers import regserialiser

class userregister(APIView):
    def post(self,request):
        k=request.data
        ser=regserialiser(data=k)    
        if ser.is_valid():
            ser.save()
            return Response('registration compleeted')
        return Response(ser.errors)        


# <--user login--->


from .serializers import LogSerializer

class Userlog(APIView):
    def post(self, request):
        user_data = request.data
        ser = LogSerializer(data=user_data)  
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user=authenticate(
            username=ser.validated_data['username'],
            password = ser.validated_data["password"]
        )
        if user is None:
            return Response({'message': 'User does not exist'}, status=404)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=200)


# <-- product users view--->

from .serializers import productserialser


class Productuserview(APIView):
    def get(self,request):
        keyword=request.GET.get('keyword')
        if keyword:
            obj=Product.objects.filter(Q(product_name__startswith=keyword)|Q(category__category_name__startswith=keyword))
        else:
            obj=Product.objects.all()
        ser=productserialser(obj,many=True) 
        return Response(ser.data)   
    


# <---wishlist users--->

from .serializers import wishlistserialiser,customerserialiser

class wishlistuserview(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        obj=wishlist.objects.all()
        ser=wishlistserialiser(obj,many=True) 
        return Response(ser.data)
    
    def post(self,request):
        k=request.data
        ser=wishlistserialiser(data=k,context={'request':request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
    
# <---cart users--->


from .serializers import cartserialiser


class cartuserview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        obj=Cart.objects.all()
        ser=cartserialiser(obj,many=True) 
        return Response(ser.data)
    
    def post(self,request):
        k=request.data
        ser=cartserialiser(data=k,context={'request':request})
        if ser.is_valid():
            ser.save()
            return Response('success')
        return Response(ser.errors)

from rest_framework import generics

class WishlistCreateView(generics.CreateAPIView):
    queryset = wishlist.objects.all()
    serializer_class = wishlistserialiser       





