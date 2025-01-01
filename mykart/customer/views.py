from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from.models import Customer_data
from django.db.models import Q


# <---user registration--->
from .serializers import Regserializer

class UserReg(APIView):
    def post(self,request):
        user_data=request.data
        serialiser=Regserializer(data=user_data)
        if serialiser.is_valid():
            serialiser.save()
            return Response('registration compleeted')
        return Response(serialiser.errors)


# <--user login--->


from .serializers import LogSerializer 

class Userlog(APIView):
    def post(self, request):
        user_data = request.data
        ser = LogSerializer(data=user_data)  
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        enterd_username = ser.validated_data["username"]
        enterd_password = ser.validated_data["password"]
        user=Customer_data.objects.filter(username=enterd_username).first()
        if user is None:
            return Response({'message': 'User does not exist'}, status=404)
        if not user.check_password(enterd_password):
            return Response ('enterd wrong password')
        return Response({'message': 'User exists'}, status=200)
