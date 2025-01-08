from rest_framework import serializers
from. models import Product,wishlist,Cart,User,Category,Orderdetails

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

    def create(self,validated_data):
        category_data=validated_data.pop('category')
        k=Category.objects.filter(category_name=category_data['category_name']).first()
        if k is None:
            k=Category.objects.create(**category_data)
        new_product=Product.objects.create(category=k,**validated_data)
        return new_product  

    def update(self, instance, validated_data):
        category_data=validated_data.pop('category',None)
        if category_data:
            k=Category.objects.filter(category_name=category_data['category_name'])
            if k is None:
                k=Category.objects.create(**category_data)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_price = validated_data.get('product_price', instance.product_price)
        instance.product_rating = validated_data.get('product_rating', instance.product_rating)
        instance.product_image = validated_data.get('product_image', instance.product_image)
        instance.save()
        return instance


# <---customer--->

class customerserialiser(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username']

# <---wishlist---->


class wishlistserialiser(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())  
    # product=productserialser()
    # customer=customerserialiser()
    class Meta:
        model=wishlist
        fields=['product','customer']


    def to_representation(self, instance):
        return {
            "product": productserialser(instance.product).data,
            "customer": instance.customer.id
    }    

    def create(self,validated_data):
        wishlist_data=wishlist.objects.create(product=validated_data['product'],customer=validated_data['customer'])
        return wishlist_data

# <---cart--->

class cartserialiser(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    # product=productserialser()
    # customer=customerserialiser()
    class Meta:
        model=Cart
        fields=['product','customer']

    def to_representation(self, instance):
        return{
            "product":productserialser(instance.product).data,
            "customer":instance.customer.id
        }    

    def create(self,validated_data):
        produc_t = validated_data['product'] 
        user= validated_data['customer']
        obj=Product.objects.filter(id=produc_t.id).first()
        cart_data=Cart.objects.create(product=obj,customer=user)        
        return cart_data
    




      

class orderserialiser(serializers.ModelSerializer):
    user= serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    product=productserialser()
    class Meta:
        model=Orderdetails
        fields=['user','product','status','payment_status','total_amount','delivery_address','date','quantity']