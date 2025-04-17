import razorpay
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Order
from customer.models import Orderdetails
import logging
import hashlib
from customer.models import Cart

RAZORPAY_KEY_ID = "rzp_test_5Tfxi7MxVhxQ7y"
RAZORPAY_SECRET = "zJfwuPE3GaOgKxPOXg6Jfv5U"
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))

logger = logging.getLogger(__name__)

# <--- Create Razorpay Order ---> 
class CreatePaymentView(APIView):
    def post(self, request):
        m=Cart.objects.filter(customer=request.user)
        print("mm--",m)

        try:
            amoun_t = request.data.get("amount")
            orde_r_id = request.data.get("id")  
            usek=request.data.get('user')        
            print("useeee-",usek)  
            j=Cart.objects.filter(customer=usek.get('id'))
            print("jjj==",j)
            amount = int(float(amoun_t) * 100)  
            currency = "INR"

            try:
                order_detail = Orderdetails.objects.get(id=orde_r_id)
            except Orderdetails.DoesNotExist:
                return Response({"error": "Invalid Orderdetails ID"}, status=status.HTTP_404_NOT_FOUND)

            payment_order = client.order.create({
                "amount": amount,
                "currency": currency,
                "payment_capture": 1
            })
            order = Order(
                order_id=payment_order['id'],
                amount=amount / 100, 
                currency=currency,
                itemOrder=order_detail
            )
            order.save()
            logger.info(f"Created payment order: {payment_order['id']}")
            return Response({
                "message": "success",
                "order_id": payment_order["id"],
                "itemOrder":orde_r_id,
                "razorpay_key": RAZORPAY_KEY_ID,
                "amount": amount,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred while creating payment order: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# <--- Verify Razorpay Payment Signature ---> 
# 

from razorpay import Utility

class VerifyPaymentView(APIView):
    def post(self, request):
        
        try:
            payment_id = request.data.get("payment_id")
            order_id = request.data.get("order_id")
            signature = request.data.get("razorpay_signature")
            user=request.data.get('user')
            print("use:=r",user)
            print('user: ',user)
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(order_id=order_id)
            order.status = 'Paid'
            cart_=Cart.objects.filter(customer=user.get('id')).first()
            # Orderdetails.objects(user=user.get('id')).delete()
            orderdetails_=Orderdetails.objects.filter(user=user.get('id')).first()
            if cart_:
                cart_.is_finished = True
                cart_.save()

            if orderdetails_:
                orderdetails_.is_finished = True
                orderdetails_.save()
                order.save()
            return Response({"message": "Payment Verified Successfully"}, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError as e:
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

