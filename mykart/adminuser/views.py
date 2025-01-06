# from django.shortcuts import render
# from rest_framework.views import APIView
# from customer.models import Customer_data,Product
# from customer.serializers import customerserialiser,productserialser
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet



# class userlistadminview(APIView):
#     def get(self,request):
#         keyword=request.GET.get('keyword')
#         if keyword:
#             k=Customer_data.objects.filter(username__startswith=keyword)
#         else:
#             k=Customer_data.objects.all()    
#         ser=customerserialiser(k,many=True)
#         return Response(ser.data)
    



# class Productadminview(ModelViewSet):
#     queryset=Product.objects.all()
#     serializer_class=productserialser
    
