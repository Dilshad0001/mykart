# payment/serializers.py
from rest_framework import serializers
from .models import Order


# <---Order--->

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'amount', 'currency', 'payment_status', 'created_at']
