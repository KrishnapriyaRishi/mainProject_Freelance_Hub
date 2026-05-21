
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from bookings.models import Booking
from chats.models import Message


@login_required
def booking_list_view(request):

    if request.user.role == 'customer':

        bookings = Booking.objects.filter(
            customer=request.user
        ).select_related(
            'provider',
            'service'
        )

    else:

        bookings = Booking.objects.filter(
            provider__user=request.user
        ).select_related(
            'customer',
            'service'
        )

    return render(
        request,
        'chatRelated/booking_list.html',
        {
            'bookings': bookings
        }
    )


@login_required
def chat_page(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    # Security validation
    is_customer = booking.customer == request.user

    is_provider = (
        booking.provider and
        booking.provider.user == request.user
    )

    if not (is_customer or is_provider):
        return render(request, '403.html')

    messages = Message.objects.filter(
        booking=booking
    ).select_related('sender').order_by('timestamp')

    return render(
        request,
        'chatRelated/chat.html',
        {
            'booking': booking,
            'messages': messages
        }
    )