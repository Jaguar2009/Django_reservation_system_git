from django.shortcuts import render, redirect
from .models import Room


def room_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms_list": rooms,
    }
    return render(
        request,
        "Booking_html/rooms_list.html",
        context=context,
    )


def get_room_by_id(request, room_id):
    room_details = Room.objects.get(id=room_id)
    context = {
        "room_detail": room_details,
    }
    return render(
        request,
        "Booking_html/room_details.html",
        context=context

    )


def about(request):
    return render(request, 'Booking_html/about.html')


def cheat_codes(request):
    if request.GET.get('access_granted') != 'true':
        return redirect('room_list')

    if request.method == 'POST':
        cheat_code = request.POST.get('cheat_code')

        if cheat_code == "0":
            request.session['background_url'] = ''
            message = 'Чіт код активований'

        if cheat_code == '/wings':
            request.session['background_url'] = 'https://kinotv.ru/upload/delight.webpconverter/upload/setka-editor/43a/13x45pm0yja8lv7ggmsj9c63co4efuom.jpg.webp?1667628389347860'
            message = 'Чіт код активований'

        if cheat_code == '/universe':
            request.session['background_url'] = 'https://i.gifer.com/Fy0t.gif'
            message = 'Чіт код активований'

        if cheat_code == "/don't/watch/it":
            request.session['background_url'] = 'https://i.gifer.com/1j64.gif'
            message = 'Чіт код активований'

        if cheat_code == "/I/want/to/go/there":
            request.session['background_url'] = 'https://ti-ukraine.org/wp-content/uploads/2021/07/maldivy.png'
            message = 'Чіт код активований'
        else:
            message = None
    else:
        message = None

    context = {
        'message': message,
    }
    return render(request, 'Booking_html/cheat_codes.html', context)




