# from django.shortcuts import render


# # Create your views here.
# def index(request):
#     return render(request, 'index.html', {})

# restaurant/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


@api_view(['GET', 'POST'])
def all_menu_items(request):
    if request.method == 'GET':
        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer=MenuSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Menu items added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
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
        serializer=BookingSerializer(request.data)
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