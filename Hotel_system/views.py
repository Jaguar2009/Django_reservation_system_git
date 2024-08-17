from django.shortcuts import render
from django.utils import timezone

from .models import Room, Booking


def room_list(reguest):
    rooms = Room.objects.all()
    context = {
        "rooms_list": rooms,
    }
    return render(
        reguest,
        "Booking_html/rooms_list.html",
        context=context,
    )