from rest_framework import serializers
from .models import Menu,Booking, User

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields='__all__'
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields='__all__'
        
class CustomerRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,style={'input_type': 'password'})
    class Meta:
        model=User
        fields=['username', 'password', 'email']
        
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user