from rest_framework import serializers
from. models import Customer_data

class Regserializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=Customer_data
        fields=['username','password','password2']
        

    def validate(self,user_data):
        if user_data['password']!=user_data['password2']:
            raise serializers.ValidationError('password doesnot match')

        return user_data
    def create(self,validated_data):
        user=Customer_data(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LogSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
