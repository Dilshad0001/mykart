from django.urls import path
from. import views

urlpatterns = [
    path('reg/',views.UserReg.as_view()),
    path('log/',views.Userlog.as_view())

]
