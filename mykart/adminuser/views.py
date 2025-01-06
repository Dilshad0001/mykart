from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Q
# <-- product users view--->

from customer .serializers import productserialser
from customer.models import Product
    

class productadminview(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=productserialser  


    def get_queryset(self):
        queryset=super().get_queryset()
        keyword=self.request.GET.get('keyword',None)
        if keyword:
            queryset=queryset.filter(Q(product_name__startswith=keyword)| Q(category__category_name__startswith=keyword))
        return queryset
        