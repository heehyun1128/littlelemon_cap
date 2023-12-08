from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
#define Serializer class for User model
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

     class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
        
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    no_of_guests=models.IntegerField(validators=[MaxValueValidator(limit_value=999999)])
    booking_date=models.DateField()
    
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    inventory=models.IntegerField(validators=[MaxValueValidator(limit_value=99999)])