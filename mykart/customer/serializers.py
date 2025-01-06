from rest_framework import serializers
from. models import Product,wishlist,Cart,User,Category

# <-- user register--->

class regserialiser(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','password','password2']


    def validate(self,user_data):
        if user_data['password']!=user_data['password2']:
            raise serializers.ValidationError('password doesnot match')

        return user_data
    def create(self,validated_data):
        user=User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user  



# <---user login--->

class LogSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()


# <---category serializers--->

class categoryserialiser(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['category_name']

# <---product--->

class productserialser(serializers.ModelSerializer):
    category=categoryserialiser()
    class Meta:
        model=Product
        fields = ['id', 'product_name', 'category','product_price', 'product_rating', 'product_image']


# <---customer--->

class customerserialiser(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['']

# <---wishlist---->
# class wishlistserialiser(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # This will receive the product ID
    # customer = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Automatically set the customer to the authenticated user
    
    # class Meta:
    #     model = wishlist
    #     fields = ['product', 'customer']

    # def create(self, validated_data):
    #     product = validated_data['product']  # This is a Product instance, not a dictionary
    #     customer = validated_data['customer']  # Automatically set by the serializer to the authenticated user
        
    #     # Create and return the wishlist entry
    #     wishlist_entry = wishlist.objects.create(product=product, customer=customer)
    #     return wishlist_entry

class wishlistserialiser(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())  
       
    # product=productserialser()
    # customer=customerserialiser()
    class Meta:
        model=wishlist
        fields=['product','customer']

    def create(self,validated_data):
        produc_t = validated_data['product'] 
        user= validated_data['customer']
        k=User.objects.filter(id=user.id).first()
        obj=Product.objects.filter(id=produc_t.id).first()
        wishlist_data=wishlist.objects.create(product=obj,customer=k)
        return wishlist_data


# <---cart--->

class cartserialiser(serializers.ModelSerializer):
    product=productserialser()
    customer=customerserialiser()
    class Meta:
        model=Cart
        fields=['product','customer']

    def create(self,validated_data):
        produc_t = validated_data['product'] 
        user= validated_data['customer']
        k=User.objects.filter(id=user.id).first()
        obj=Product.objects.filter(id=produc_t.id).first()
        cart_data=wishlist.objects.create(product=obj,customer=k)        
        return cart_data
    




      