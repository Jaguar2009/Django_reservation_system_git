from django.db import models
from django.contrib.auth.models import User
import secrets
import hashlib


class Hotel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    location = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.rating}'

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"
        ordering = ["rating"]


class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Вільна'),
        ('booked', 'Заброньована'),
        ('unavailable', 'Не доступна'),
    ]

    number = models.IntegerField()
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["number"]

    def __str__(self):
        return f'Room №{self.number} - {self.capacity} - ({self.status})'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=64, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["start_date"]

    def __str__(self):
        return f'{self.user} - {self.room}'

    def generate_verification_code(self):
        code = secrets.token_hex(4)
        self.verification_code = hashlib.sha256(code.encode()).hexdigest()
        self.save()
        return code

