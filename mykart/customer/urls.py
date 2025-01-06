from django.urls import path,include
from. import views
# from adminuser.views import 
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'a', Productadminview, basename='adminview')
# urlpatterns = router.urls

urlpatterns = [
    path('log/',views.Userlog.as_view()),
    path('ghj/',views.Productuserview.as_view()),
    path('',views.wishlistuserview.as_view()),
    path('ede/',views.cartuserview.as_view()),
    # path('k/',userlistadminview.as_view()),
    # path('n/',include(router.urls)),
    path('mm/',views.WishlistCreateView.as_view()),
    path('ll/',views.userregister.as_view())



]
