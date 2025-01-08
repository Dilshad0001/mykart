from django.contrib import admin
from . models import Category,Product,wishlist,Cart,User,Orderdetails

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(wishlist)
admin.site.register(Cart)
admin.site.register(User)
admin.site.register(Orderdetails)


# Register your models here.
