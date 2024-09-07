from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Hotel, Booking
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class BookingForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ця електронна пошта вже використовується.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


def hotel_list(request):
    hotels = Hotel.objects.all()
    context = {
        "hotels_list": hotels,
    }
    return render(
        request,
        "Booking_html/hotels_list.html",
        context=context,
    )


def hotel_rooms_list_details(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)

    query = request.GET.get('q', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    capacity_from = request.GET.get('capacity_from')
    capacity_to = request.GET.get('capacity_to')

    if query:
        rooms = rooms.filter(name__icontains=query)

    if price_from and price_to:
        rooms = rooms.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        rooms = rooms.filter(price__gte=price_from)
    elif price_to:
        rooms = rooms.filter(price__lte=price_to)

    if capacity_from and capacity_to:
        rooms = rooms.filter(capacity__gte=capacity_from, capacity__lte=capacity_to)
    elif capacity_from:
        rooms = rooms.filter(capacity__gte=capacity_from)
    elif capacity_to:
        rooms = rooms.filter(capacity__lte=capacity_to)

    context = {
        'hotel': hotel,
        'rooms': rooms,
    }
    return render(request, 'Booking_html/hotel_rooms_list_details.html', context)


def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    context = {
        'room': room,
    }
    return render(request, 'Booking_html/room_details.html', context)


@login_required
def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room

            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_date__lt=booking.end_date,
                end_date__gt=booking.start_date
            )

            if overlapping_bookings.exists():
                form.add_error(None, "Ця кімната вже заброньована на зазначений період.")
            else:
                room.status = 'booked'
                room.save()
                booking.save()
                return redirect('my_bookings')
    else:
        form = BookingForm()

    return render(request, 'Booking_html/booking_form.html', {'form': form, 'room': room})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'Booking_html/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    room = booking.room
    booking.delete()
    room.status = 'available'
    room.save()
    return redirect('my_bookings')


def about(request):
    return render(request,
                  'Booking_html/about.html')


def hotel_search(request):
    query = request.GET.get('q', '')
    rating_from = request.GET.get('rating_from')
    rating_to = request.GET.get('rating_to')

    hotels = Hotel.objects.all()

    if query:
        hotels = hotels.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if rating_from and rating_to:
        hotels = hotels.filter(rating__gte=rating_from, rating__lte=rating_to)
    elif rating_from:
        hotels = hotels.filter(rating__gte=rating_from)
    elif rating_to:
        hotels = hotels.filter(rating__lte=rating_to)

    context = {
        'hotels': hotels,
    }
    return render(request, 'Booking_html/hotel_search_results.html', context)


def activate_cheat_code(request, cheat_code, background_url, redirect_url):
    if request.POST.get('cheat_code') == cheat_code:
        request.session['background_url'] = background_url
        return redirect(redirect_url)


def cheat_codes(request):
    if request.GET.get('access_granted') != 'true':
        return redirect('hotel_list')

    if 'cheat_code' in request.POST:
        cheat_code = request.POST['cheat_code']

        if cheat_code == "0":
            return activate_cheat_code(request, "0", '', 'hotel_list')

        if cheat_code == '/wings':
            return activate_cheat_code(
                request,
                '/wings',
                'https://kinotv.ru/upload/delight.webpconverter/upload/setka-editor/43a/13x45pm0yja8lv7ggmsj9c63co4efuom.jpg.webp?1667628389347860',
                'hotel_list'
            )

        if cheat_code == '/universe':
            return activate_cheat_code(
                request,
                '/universe',
                'https://i.gifer.com/Fy0t.gif',
                'hotel_list'
            )

        if cheat_code == "/don't/watch/it":
            return activate_cheat_code(
                request,
                "/don't/watch/it",
                'https://i.gifer.com/1j64.gif',
                'hotel_list'
            )

        if cheat_code == "/I/want/to/go/there":
            return activate_cheat_code(
                request,
                "/I/want/to/go/there",
                'https://ti-ukraine.org/wp-content/uploads/2021/07/maldivy.png',
                'hotel_list'
            )
    return render(request,
                  'Booking_html/cheat_codes.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('hotel_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'Booking_html/register.html', context={'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('hotel_list')
            else:
                messages.error(request, 'Неправильний логін або пароль')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'Booking_html/login.html', context)


@login_required(login_url='register/')
def user_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'Booking_html/user_profile.html', context)


def user_logout(request):
    logout(request)
    return redirect('hotel_list')
