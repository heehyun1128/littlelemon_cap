# #define URL route for index() view
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='index')
# ]




from django.urls import path
from . import views

urlpatterns = [
    path('menu/',views.all_menu_items,name='views.all_menu_items'),
    path('menu/<int:pk>/',views.single_menu_item,name='views.single_menu_item'),
    path('booking/',views.all_bookings,name='views.all_bookings'),
    path('booking/<int:pk>/',views.single_booking,name='views.single_booking'),
   
]