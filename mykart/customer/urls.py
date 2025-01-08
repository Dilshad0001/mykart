from django.urls import path,include
from. import views
# from adminuser.views import 
from rest_framework.routers import DefaultRouter
from adminuser.views import productadminview,adminuserlistview


# router = DefaultRouter()
# router.register(r'a', Productadminview, basename='adminview')
# urlpatterns = router.urls
router = DefaultRouter()
router.register('product', productadminview, basename='product')
urlpatterns = [
    path('log/',views.Userlog.as_view()),
    path('g/',views.Productuserview.as_view()),
    path('hj/',views.wishlistuserview.as_view()),
    path('ede/',views.cartuserview.as_view()),
    # path('k/',userlistadminview.as_view()),
    # path('n/',include(router.urls)),
    # path('mm/',views.WishlistCreateView.as_view()),
    path('ll/',views.userregister.as_view()),
    path('jhg/', include(router.urls)),
    path('joo/',adminuserlistview.as_view()),
    path('kjsk/',views.orderuserview.as_view()),
    path('',views.orderadminview.as_view()),


]