from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.hotel_rooms_list_details, name='hotel_rooms_list_details'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('cheat_codes/', views.cheat_codes, name='cheat_codes'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('about/', views.about, name='about'),
    path('hotel_search/', views.hotel_search, name='hotel_search'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),

    ]
