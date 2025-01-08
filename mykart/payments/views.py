# payment/views.py
import razorpay
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer

# Razorpay API Keys
RAZORPAY_KEY_ID = "rzp_test_5Tfxi7MxVhxQ7y"
RAZORPAY_SECRET = "zJfwuPE3GaOgKxPOXg6Jfv5U"
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))

class CreatePaymentView(APIView):
    def post(self, request):
        try:
            amoun_t = request.data.get("amount")
            amount=amoun_t*100 # Convert to paise
            currency = "INR"

            # Razorpay Order API
            payment_order = client.order.create({
                "amount": amount,
                "currency": currency,
                "payment_capture": 1  # Auto capture
            })

            # Save order to DB
            order = Order(
                order_id=payment_order['id'],
                amount=amount / 100,  # Convert back to INR
                currency=currency
            )
            order.save()

            # Response to frontend
            return Response({
                "order_id": payment_order["id"],
                "razorpay_key": RAZORPAY_KEY_ID,
                "amount": amount,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
