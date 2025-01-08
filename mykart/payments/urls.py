from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreatePaymentView.as_view(), name='create_payment'),
]
