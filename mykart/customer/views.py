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
            'message':"login sucess",
            # 'user':user
        }, status=200)
    

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff
        })    

# class current_user(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
#         return Response ({"id":request.user.id,"username":request.user.username})

class current_user(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "is_admin": request.user.is_superuser,  # <-- add this
            "is_staff": request.user.is_staff       # <-- optional
        })
# <-- product users view--->

from .serializers import productserialser


class Productuserview(APIView):
    def get(self,request):
        keyword=request.GET.get('keyword')
        product_id=request.GET.get('id')
        if keyword :
            obj=Product.objects.filter(Q(product_name__startswith=keyword)|Q(category__category_name__startswith=keyword))
        elif product_id:
            obj=Product.objects.filter(id=product_id)
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
        obj=Cart.objects.filter(customer=request.user)
        ser=cartserialiser(obj,many=True) 
        return Response(ser.data)
    
    def post(self,request):
        print("strtedd")
        user_=request.user
        k=request.data
        print("reqqqq===",request.data)
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
        sub_total_amount=data_.get('sub_total_amount')
        if new_count is None and sub_total_amount is None:
            return Response("data is missing") 
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




# <---order details-->
from .models import Orderdetails
from .serializers import orderserialiser,orderserialiseradmin


class orderuserview(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request):
        k=Orderdetails.objects.filter(user=request.user, is_finished=False)
        if k is None:
            return Response('no data found')
        ser=orderserialiser(k,many=True)
        return Response(ser.data)
            

    def post(self, request):
        cart_id=request.data.get('carts')      
        if cart_id is None :
            return Response('cart id  requierd')
        ser=orderserialiser(data=request.data,context={'request':request})
        if ser.is_valid():
            ser.save()
            return Response("done")
        
        return Response(ser.errors)


    

# <-- order details admin view--->
    
class orderadminview(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        keyword=request.GET.get('user')
        if keyword:
            obj=Orderdetails.objects.filter(user__username__startswith=keyword).order_by("-id")
        else:
            obj=Orderdetails.objects.all()
        ser=orderserialiseradmin(obj,many=True)
        return Response(ser.data)        
    def put(self,request):
        k=request.data
        order_data=Orderdetails.objects.filter(id=k['order_id']).first()
        if order_data is None:
            return Response('order not found')
        cust=User.objects.get(orderdetails__id=k['order_id'])
        cust.order_number=cust.order_number+1
        cust.save()
        print("custt",request.data)
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
