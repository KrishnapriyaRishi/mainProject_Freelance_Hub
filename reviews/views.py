
from django.shortcuts import render,redirect
from accounts.views import dashboard
from .models import Review
from bookings.models import Booking


def submit_review(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == "POST":
        Review.objects.create(booking=booking,customer=request.user,provider=booking.provider,
                              rating=request.POST.get('rating'),comment=request.POST.get('comment'))
        booking.is_reviewed=True
        booking.save()
        return redirect(dashboard)
    else:
        
    	return render(request,"reviewRelated/review.html")