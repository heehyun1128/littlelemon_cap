#define URL route for index() view
from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.index, name='index')
# ]




from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

# urlpatterns = [
    
#     path('login/', views.login_view, name='login_view'),
#     path('logout/', views.logout_view, name='logout_view'),
#     path('menu/',views.all_menu_items,name='all_menu_items'),
#     path('menu/<int:pk>/',views.single_menu_item,name='single_menu_item'),
#     path('booking/',views.all_bookings,name='all_bookings'),
#     path('booking/<int:pk>/',views.single_booking,name='single_booking'),
#     path('api-token-auth/', obtain_auth_token),
#     path('', views.index, name='home'),
#     path('about', views.about, name='about'),
#     path('reservations', views.reservations, name='reservations'),
#     path('book_page', views.book_page, name='book_page'),
#     path('menu_page', views.menu_page, name='menu_page'),
   
# ]
urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('register/', views.register, name="register"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.single_menu_item, name="menu_item"),  
    path('bookings/', views.bookings, name='bookings'), 
    # path('logout/', views.logout_view, name='logout'),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
]