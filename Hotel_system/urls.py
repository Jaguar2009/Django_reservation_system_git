from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name="room_list"),
    path('<int:room_id>/', views.get_room_by_id, name='room_details'),
    path('cheat_codes/', views.cheat_codes, name='cheat_codes'),
    path('about/', views.about, name='about'),

    ]