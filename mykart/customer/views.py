from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from.models import Product,wishlist,Cart,User,Category
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status



# <---user registration--->

from .serializers import regserialiser

class userregister(APIView):
    def post(self,request):
        k=request.data
        ser=regserialiser(data=k)    
        if ser.is_valid():
            ser.save()
            return Response({"messages": "registration completed"}, status=status.HTTP_201_CREATED)
        print(ser.errors)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)  
      


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
            'message':"login sucess"
        }, status=200)


# <-- product users view--->

from .serializers import productserialser


class Productuserview(APIView):
    def get(self,request):
        keyword=request.GET.get('keyword')
        product_id=request.GET.get('id')
        if keyword:
            obj=Product.objects.filter(Q(product_name__startswith=keyword)|Q(category__category_name__startswith=keyword))
        elif product_id:
            obj=Product.objects.filter(id=product_id)
        else:
            obj=Product.objects.all()

        ser=productserialser(obj,many=True)      
        return Response(ser.data)   
    # def patch(self,request):
    #     data_=request.data
    #     quantity_change=data_.quantityChange
    #     product_id=data_.productId
    #     ins=Product.objects.get(id=product_id)
    #     k=ins.quantity+quantity_change
    #     ser=productserialser(ins,data=quantity_change,partial=True)

    


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
        obj=Cart.objects.filter(customer=request.user)
        ser=cartserialiser(obj,many=True) 
        return Response(ser.data)
    
    def post(self,request):

        user_=request.user
        k=request.data
        print("kk--",k.get('product'))
        m=Cart.objects.filter(product__id=k.get('product'),customer=user_).first()
        if m is not None:
            m.count=m.count+1

            m.save()
            ser = cartserialiser(m, context={'request': request})
            return Response(ser.data)
        ser=cartserialiser(data=k,context={'request':request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    def patch(self,request):
        user_=request.user
        data_=request.data
        cart_id=data_.get('order_id')
        if cart_id is None:
            return Response(" order_id requierd ")    
        ins=Cart.objects.get(id=cart_id)
        new_count=data_.get('count')
        if new_count is None:
            return Response("enter count") 
        ser=cartserialiser(ins,data=data_,partial=True)
        if ser.is_valid():
            ser.save()
            return Response("done")
        return Response(ser.errors)
    
    def delete(self,request):
        use_r=request.user
        k=request.data
        obj=k['id']
        dat_a=Cart.objects.filter(customer=use_r,id=obj)
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
        if not quantity:
            quantity=1        
        if not product_id :
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
    permission_classes=[IsAdminUser]
    def get(self,request):
        keyword=request.GET.get('user')
        if keyword:
            obj=Orderdetails.objects.filter(user__username__startswith=keyword)
        else:
            obj=Orderdetails.objects.all()
        ser=orderserialiseradmin(obj,many=True)
        return Response(ser.data)        
    def put(self,request):
        k=request.data
        order_data=Orderdetails.objects.filter(id=k['order_id']).first()
        if order_data is None:
            return Response('order not found')
        ser=orderserialiseradmin(order_data,data=k,partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
    
from .serializers import categoryserialiser

class CategoryUserView(APIView):
    def get(self,request):
        data=Category.objects.all()
        ser=categoryserialiser(data,many=True)
        return Response(ser.data)