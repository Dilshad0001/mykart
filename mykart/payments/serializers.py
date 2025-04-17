# payment/serializers.py
from rest_framework import serializers
from .models import Order
from customer.serializers import orderserialiser
from customer.models import Orderdetails


# <---Order--->

class OrderSerializer(serializers.ModelSerializer):
    itemOrder=serializers.PrimaryKeyRelatedField(queryset=Orderdetails.objects.all()) 
    class Meta:
        model = Order
        fields = ['id','order_id','itemOrder', 'amount', 'currency', 'created_at','status']
