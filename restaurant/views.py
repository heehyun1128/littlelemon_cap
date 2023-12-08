# from django.shortcuts import render


# # Create your views here.
# def index(request):
#     return render(request, 'index.html', {})

# restaurant/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny]) 
def customer_register_view(request):
    if request.method=='POST':
        serializer=CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    
    username=request.data.get('username')
    password=request.data.get('password')
    
    if not username or not password:
        return Response({'message': 'Both username and password are required.'}, status=400)

    user=authenticate(request,username=username,password=password)
    
    if user is not None:
        login(request,user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
# log out
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.auth:
        request.auth.delete()
    logout(request)
    return Response({'message': 'Logout successful'}, status=200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def all_menu_items(request):
    if request.method == 'GET':
        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'error':'You do not have the authorization to perform this action.'},status=status.HTTP_403_FORBIDDEN)
        
        serializer=MenuSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Menu items added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) 
def single_menu_item(request,pk):
    try:
        menu_item = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response({'message': 'Item not found'}, status=404)

    if request.method == 'GET':
        serializer = MenuSerializer(menu_item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MenuSerializer(menu_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Menu item updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        menu_item.delete()
        return Response({'message': 'Menu Item Deleted Successfully.'}, status=status.HTTP_200_OK)
    
# booking routes
@api_view(['GET', 'POST'])
def all_bookings(request):
    if request.method == 'GET':
        booking_items = Booking.objects.all()
        serializer = BookingSerializer(booking_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer=BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def single_booking(request,pk):
    try:
        booking_item = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response({'message': 'Item not found'}, status=404)

    if request.method == 'GET':
        serializer = BookingSerializer(booking_item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookingSerializer(booking_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        booking_item.delete()
        return Response({'message': 'Booking Deleted Successfully.'}, status=status.HTTP_200_OK)