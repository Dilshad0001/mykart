from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Q
from customer.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser


# <-- product users view--->

from customer .serializers import productserialser
from customer.models import Product
    

# class productadminview(ModelViewSet):
#     # permission_classes=[IsAdminUser]
#     # k=request.data
#     queryset=Product.objects.all()
#     serializer_class=productserialser

#     def create(self, request, *args, **kwargs):
#         k = request.data
#         print("Received data:", k) 
#         print("Received name:", k['product_name']) 
#         print("Received price:", k['product_price'])
#         serializer = self.get_serializer(data=k)
#         if serializer.is_valid():
#             product=serializer.save()
#             return Response("added succes fully")
#         return Response ("validation failed")

class productadminview(APIView):
    # permission_classes=[IsAdminUser]
    def get(self,request):
        print("getttx   ")
        k=Product.objects.all()
        ser=productserialser(k,many=True)
        return Response(ser.data)
    def post(self,request):
        print("postt",request.data)
        ser=productserialser(data=request.data)
        print("startt-")
        if ser.is_valid():
            ser.save()
            print("succ-")
            return Response("product added")
        print("failed-")
        return Response(ser.errors)
    def put(self,request):
        updated_product=request.GET.get("updateId")
        print("start==",request.data)
        print("kkkk,",type(updated_product))
        g=updated_product
        

        cleaned_update_id = updated_product.replace(":", "") 
        try:
            
            ins=Product.objects.get(id=int(cleaned_update_id))
            print("inss",ins)
        except:
            print("ggggggg")
            return Response("enter valid id")
        ser=productserialser(ins,data=request.data,partial=True)
        print("after ser")
        if ser.is_valid():
            ser.save()
            print("suceee")
            return Response("product data updated")
        print("ffffffff",ser.errors)
        return Response(ser.errors)  
    def delete(self,request):
        k=request.data
        obj=k['id']
        dat_a=Product.objects.filter(id=obj)
        if dat_a is None:
            return Response('no data found')
        dat_a.delete()
        return Response('data_deleted')  




    # def get_queryset(self):
    #     queryset=super().get_queryset()
    #     keyword=self.request.GET.get('keyword',None)
    #     if keyword:
    #         queryset=queryset.filter(Q(product_name__startswith=keyword)| Q(category__category_name__startswith=keyword))
    #     return queryset


# <---admi users list view--->


from customer.serializers import customerserialiser

class adminuserlistview(APIView):
    # permission_classes=[IsAdminUser]
    def get(self,request):
        # keyword=request.GET.get('keyword')
        # if keyword:
            # users_data=User.objects.filter(username__startswith=keyword)
        # else:
        users_data=User.objects.all()    
        ser=customerserialiser(users_data,many=True)
        return Response (ser.data)
    def put(self,request):
        print("userdata----",request.data)
        data_=request.data
        print(data_.get('is_active'))
        user_id=request.data.get('id')
        print('user id --',user_id)
        user_data=User.objects.get(id=user_id)
        print('user_data', user_data.is_active)
        user_data.is_active = data_.get('is_active')
        # if data_.get('is_active')==0:
        #     user_data.is_active=True
        #     print("kk", user_data.is_active)
        ser=customerserialiser(user_data,data=request.data,partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    


class admin_home(APIView):

    def get(self,request):
        return Response("welcome admin home")