from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("The Username field must be set.")
        user = self.model(username=username)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"   
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.username



# class Customer_data(AbstractBaseUser):
#     username=models.CharField(max_length=100)

#     def __str__(self):
#         return self.username




class Category(models.Model):
    category_name=models.CharField(max_length=20)

    def __str__(self):
        return self.category_name



class Product(models.Model):
    product_name=models.CharField(max_length=20)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_rating=models.IntegerField(null=True)
    product_price = models.IntegerField()
    product_image=models.ImageField(upload_to='image/',null=True)

    def __str__(self):
        return self.product_name


    

class wishlist(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.product.product_name
    

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    count=models.IntegerField(default=1)


    def __str__(self):
        return self.product.product_name    
    

from datetime import datetime

class Orderdetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)  
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
    ])
    payment_status = models.CharField(max_length=20, choices=[
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ])
    total_amount=models.IntegerField()
    delivery_address=models.TextField()
    date=models.DateTimeField(default=datetime.now)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

