from django.urls import path,include
from. import views
# from adminuser.views import 
from rest_framework.routers import DefaultRouter
from adminuser.views import productadminview,adminuserlistview


router = DefaultRouter()
router.register('product', productadminview, basename='product')
urlpatterns = [

#   user register and login
    path('log/',views.Userlog.as_view()),
    path('reg/',views.userregister.as_view()),
    path('users/',adminuserlistview.as_view()),
    path('current/',views.current_user.as_view()),

# category
    path('category/',views.CategoryUserView.as_view()),


# product
    path('product/',views.Productuserview.as_view()),
    path('adminproduct/', include(router.urls)),

#  order, wishlist & cart 
    path('wishlist/',views.wishlistuserview.as_view()),
    path('cart/',views.cartuserview.as_view()),
    path('order/',views.orderuserview.as_view()),
    path('adminorder/',views.orderadminview.as_view()),
    
]