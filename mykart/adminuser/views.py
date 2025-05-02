from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Q
from customer.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



# <-- product users view--->

from customer .serializers import productserialser
from customer.models import Product
    


class productadminview(APIView):
    permission_classes=[IsAdminUser]


    def get(self, request):
        products = Product.objects.all().order_by("-id")

        paginator = PageNumberPagination()
        paginator.page_size = 5  
        result_page = paginator.paginate_queryset(products, request)

        serializer = productserialser(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self,request):
        ser=productserialser(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("product added")
        print("failed-")
        return Response(ser.errors)
    def put(self,request):
        updated_product=request.GET.get("updateId")
        # g=updated_product
        cleaned_update_id = updated_product.replace(":", "") 
        try:
            
            ins=Product.objects.get(id=int(cleaned_update_id))
        except:
            return Response("enter valid id")
        ser=productserialser(ins,data=request.data,partial=True)
        if ser.is_valid():
            ser.save()
            return Response("product data updated")
        return Response(ser.errors)  
    def delete(self,request):
        k=request.data
        obj=k['id']
        dat_a=Product.objects.filter(id=obj)
        if dat_a is None:
            return Response('no data found')
        dat_a.delete()
        return Response('data_deleted')  



from customer.serializers import customerserialiser


from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'  
    max_page_size = 100 

class adminuserlistview(APIView):
    permission_classes=[IsAdminUser]
    def get(self, request):
        users_data = User.objects.all()
        
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users_data, request)
        
        ser = customerserialiser(result_page, many=True)
        return paginator.get_paginated_response(ser.data)

    def put(self,request):
        data_=request.data
        user_id=request.data.get('id')
        user_data=User.objects.get(id=user_id)
        user_data.is_active = data_.get('is_active')
        ser=customerserialiser(user_data,data=request.data,partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    


class admin_home(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        return Response("welcome admin home")