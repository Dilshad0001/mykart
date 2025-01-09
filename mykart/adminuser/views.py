from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Q
from customer.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser


# <-- product users view--->

from customer .serializers import productserialser
from customer.models import Product
    

class productadminview(ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=Product.objects.all()
    serializer_class=productserialser  


    def get_queryset(self):
        queryset=super().get_queryset()
        keyword=self.request.GET.get('keyword',None)
        if keyword:
            queryset=queryset.filter(Q(product_name__startswith=keyword)| Q(category__category_name__startswith=keyword))
        return queryset


# <---admi users list view--->


from customer.serializers import customerserialiser

class adminuserlistview(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        keyword=request.GET.get('keyword')
        if keyword:
            users_data=User.objects.filter(username__startswith=keyword)
        else:
            users_data=User.objects.all()    
        ser=customerserialiser(users_data,many=True)
        return Response (ser.data)