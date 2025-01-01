from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


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
    
