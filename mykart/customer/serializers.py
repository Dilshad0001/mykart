from rest_framework import serializers
from. models import Product,wishlist,Cart,User,Category,Orderdetails

# <-- user register--->

class regserialiser(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','password','password2','is_active','is_staff','is_superuser']


    def validate(self,user_data):
        if user_data['password']!=user_data['password2']:
            raise serializers.ValidationError({"message":"password is not match"})

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
        fields=['id','category_name','category_image']

# <---product--->

class productserialser(serializers.ModelSerializer):
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    class Meta:
        model=Product
        fields = ['id', 'product_name', 'category','product_price', 'product_image','created_at','product_decription']

    def to_representation(self, instance):
        return {
            "id":instance.id,
            "product_name":instance.product_name,
            "category":categoryserialiser(instance.category).data,
            "product_price":instance.product_price,
            "product_image": instance.product_image.url if instance.product_image else None,
            "created_at":instance.created_at,
            "product_decription":instance.product_decription


        }    

    def create(self,validated_data):
        category_data=validated_data.pop('category')
        print("im here...")
        k=Category.objects.filter(id=category_data.id).first()
        if k is None:
            raise serializers.ValidationError("no category found")
        new_product=Product.objects.create(category=k,**validated_data)
        return new_product  

    def update(self, instance, validated_data):
        categoryIns=validated_data.get('category')
        # print("vvv", h.id)
        category_data=validated_data.pop('category',None)
        if categoryIns:
            k=Category.objects.filter(id=categoryIns.id)
            if k is None:
                k=Category.objects.create(**categoryIns)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_price = validated_data.get('product_price', instance.product_price)
        instance.product_image = validated_data.get('product_image', instance.product_image)
        instance.product_decription=validated_data.get('product_decription',instance.product_decription)
        instance.category=categoryIns   
        instance.save()
        return instance


# <---customer--->

class customerserialiser(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','user_email','order_number','is_active']

# <---wishlist---->


class wishlistserialiser(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
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
        # print(self.context['request'].user,"......")
        return wishlist_data

# <---cart--->

class cartserialiser(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault()) 

    class Meta:
        model=Cart
        fields=['id','product','customer','count','sub_total_amount','is_finished']

    def to_representation(self, instance):
        return{
            "order_id":instance.id,
            "product":productserialser(instance.product).data,
            "customer":instance.customer.id,
            "count":instance.count,
            "total":instance.sub_total_amount,
            "is_finished":instance.is_finished
            
        }    

    def create(self,validated_data):
        produc_t = validated_data['product'] 
        user= validated_data['customer']
        coun_t=validated_data.get('count',1)
        obj=Product.objects.filter(id=produc_t.id).first()
        cart_data=Cart.objects.create(product=obj,count=coun_t,customer=user)        
        return cart_data
    def update(self, instance, validated_data):
        print("hhhhhhh")
        instance.count=validated_data.get('count',instance.count)
        instance.sub_total_amount=validated_data.get('sub_total_amount',instance.sub_total_amount)
        instance.save()
        return instance
    




      

class orderserialiser(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    carts = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(),many=True)

    class Meta:
        model = Orderdetails
        fields = ['id', 'user', 'carts', 'status', 'payment_status', 'total_amount', 'delivery_address', 'date','is_finished']

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "carts": cartserialiser(instance.carts.all(), many=True).data,
            # "carts": cartserialiser(instance.carts.all(), many=True).data,
            # "carts":cartserialiser(instance.carts).data,
            "status": instance.status,
            "payment_status": instance.payment_status,
            "total_amount": instance.total_amount,
            "delivery_address": instance.delivery_address,
            "date": instance.date
        }

    def create(self, validated_data):
        carts_data = validated_data.pop('carts')  # pop out M2M data
        new_order = Orderdetails.objects.create(**validated_data)
        new_order.carts.set(carts_data)  # assign M2M after creating
        return new_order




 
# class orderserialiseradmin(serializers.ModelSerializer):
#     user=customerserialiser()
#     carts=cartserialiser()
#     class Meta:
#         model=Orderdetails
#         fields=['id','user','carts','status','payment_status','total_amount','delivery_address','date','is_finished']     

#     def update(self,instance,validated_data):
#         instance.payment_status=validated_data.get('payment_status',instance.payment_status)   
#         instance.status=validated_data.get('status',instance.status)
#         instance.save()
#         return instance

class orderserialiseradmin(serializers.ModelSerializer):
    user = customerserialiser()
    carts = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(),many=True)

    class Meta:
        model = Orderdetails
        fields = ['id', 'user', 'carts', 'status', 'payment_status', 'total_amount', 'delivery_address', 'date','is_finished']

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "carts": cartserialiser(instance.carts.all(), many=True).data,
            # "carts": cartserialiser(instance.carts.all(), many=True).data,
            # "carts":cartserialiser(instance.carts).data,
            "user":customerserialiser(instance.user).data,
            "status": instance.status,
            "payment_status": instance.payment_status,
            "total_amount": instance.total_amount,
            "delivery_address": instance.delivery_address,
            "date": instance.date,
            "is_finished":instance.is_finished
        }

    def create(self, validated_data):
        carts_data = validated_data.pop('carts')  # pop out M2M data
        new_order = Orderdetails.objects.create(**validated_data)
        new_order.carts.set(carts_data)  # assign M2M after creating
        return new_order
    def update(self, instance, validated_data):
        print("vaal", validated_data)
        instance.payment_status=validated_data.get('payment_status',instance.payment_status)
        instance.status=validated_data.get('status',instance.status)
        instance.is_finished=validated_data.get('is_finished',instance.is_finished)
        instance.save()
        print("inss", instance.status)
        return instance