from django.shortcuts import render,redirect
from .forms import BookingForm
from datetime import datetime
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# restaurant/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib import messages
# from .forms import NewUserForm
# Create your views here.
# def index(request):
#     return render(request, 'index.html')
# def book_page(request):
#     return render(request, 'book.html')
# def menu_page(request):
#     return render(request, 'menu.html')
# def about(request):
#     return render(request, 'about.html')
# def reservations(request):
#     return render(request, 'bookings.html')

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})



@api_view(['GET','POST'])
@permission_classes([AllowAny]) 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

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
@permission_classes([IsAuthenticated]) 
def bookings(request):
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
@permission_classes([IsAuthenticated]) 
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