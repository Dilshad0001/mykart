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
        use_r=request.user
        obj=wishlist.objects.filter(customer=use_r)
        ser=wishlistserialiser(obj,many=True) 
        return Response(ser.data)

    def post(self, request):
        serializer = wishlistserialiser(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)   

    def delete(self,request):
        use_r=request.user
        k=request.data
        obj=k['product']
        dat_a=wishlist.objects.filter(customer=use_r,product=obj)
        if dat_a is None:
            return Response('no data found')
        dat_a.delete()
        return Response('data_deleted') 
    
    
# <---cart users--->


from .serializers import cartserialiser


class cartuserview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # k=request.user
        obj=Cart.objects.filter(customer=request.user)
        ser=cartserialiser(obj,many=True) 
        return Response(ser.data)
    
    def post(self,request):
        k=request.data
        ser=cartserialiser(data=k,context={'request':request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
    def delete(self,request):
        use_r=request.user
        k=request.data
        obj=k['product']
        dat_a=Cart.objects.filter(customer=use_r,product=obj)
        if dat_a is None:
            return Response('no data found')
        dat_a.delete()
        return Response('data_deleted')


# from rest_framework import generics

# class WishlistCreateView(generics.CreateAPIView):
#     queryset = wishlist.objects.all()
#     serializer_class = wishlistserialiser       





# <---order details-->
from .models import Orderdetails
from .serializers import orderserialiser,orderserialiseradmin


class orderuserview(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request):
        k=Orderdetails.objects.filter(user=request.user)
        if k is None:
            return Response('no data found')
        ser=orderserialiser(k,many=True)
        return Response(ser.data)
            

    def post(self, request):
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity')
        if not product_id:
            return Response('product id and quantity requierd')
        try:
            produc_t=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response ('product doesnot exist')
        total_price=produc_t.product_price*int(quantity)  
        order=Orderdetails.objects.create(
            user=request.user,
            product=produc_t,
            quantity=quantity,
            total_amount=total_price,
            payment_status='pending',
            status='Pending'
        )
        ser=orderserialiser(order) 
        return Response(ser.data)
    

# <-- order details admin view--->
    
class orderadminview(APIView):
    def get(self,request):
        keyword=request.GET.get('keyword')
        if keyword:
            obj=Orderdetails.objects.filter(user__username__startswith=keyword)
        else:
            obj=Orderdetails.objects.all()
        ser=orderserialiseradmin(obj,many=True)
        return Response(ser.data)        
    def put(self,request):
        k=request.data
        order_data=Orderdetails.objects.filter(id=k['id']).first()
        if order_data is None:
            return Response('order not found')
        ser=orderserialiseradmin(order_data,data=k,partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
        


