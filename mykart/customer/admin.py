from django.contrib import admin
from . models import Category,Product,wishlist,Cart,User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(wishlist)
admin.site.register(Cart)
admin.site.register(User)


# Register your models here.
