import random
from django.shortcuts import render,redirect
from .models import Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from services.models import Service
from accounts.models import ServiceProviderProfile
from accounts.views import *
from notifications.models import Notification


# Create your views here.
def assign_provider(service_cat):
    providers = ServiceProviderProfile.objects.filter(service_field=service_cat,is_verified=True,availabilty_status='available')
    if not providers.exists():
        return None
    return random.choice(providers)



@login_required(login_url='/accounts/login')
def create_booking(request, sId):
    ser = Service.objects.get(id=sId)
    
    if request.method == 'POST':
        # Pass the entire POST dictionary to a single form instance
        form = BookingForm(request.POST)
        
        if form.is_valid():
            try:
                provider = assign_provider(ser.category)
                if not provider:
                    raise Exception("No provider available")
                
                # Commit=False creates the object but doesn't save it to the DB yet
                booking = form.save(commit=False)
                
                # Manually assign the relationships not handled by the form fields
                booking.customer = request.user
                booking.provider = provider
                booking.service = ser
                booking.status ='pending'
                
                # Save the complete object to the database
                booking.save()
                
                print("Booking done successfully!.")
                return redirect(dashboard) 
                
            except Exception as e:
                # Handle the missing provider exception 
                messages.error(request, str(e))
    else:
        
        form = BookingForm(initial={})
        
    return render(request, "bookingRelated/bookingForm.html", {'form': form,'service':ser})


@login_required(login_url='/accounts/login')
def display_providerAcceptedBooking(request):
    ser_p = ServiceProviderProfile.objects.get(user=request.user)
    booking = Booking.objects.filter(provider=ser_p)
    return render(request,"bookingRelated/acceptedBooking.html",{'bookings':booking})



@login_required(login_url='/accounts/login')
def provider_acceptBooking(request,bookId):
    booking = Booking.objects.get(id=bookId)
    booking.status="accepted"
    booking.save()
    Notification.objects.create(receiver=booking.customer,title="Booking Accepted",message=f"{booking.provider.user.username} accepted your booking")
    return redirect(display_providerAcceptedBooking)



@login_required(login_url='/accounts/login')
def provider_startWork(request,bookId):
    booking = Booking.objects.get(id=bookId)
    booking.status="in_progress"
    booking.save()
    Notification.objects.create(receiver=booking.customer,title="Work Started",message=f"Your service provider started the work.")
    return redirect(display_providerAcceptedBooking)



@login_required(login_url='/accounts/login')
def provider_completedWork(request,bookId):
    booking = Booking.objects.get(id=bookId)
    booking.status="completed"
    booking.save()
    Notification.objects.create(receiver=booking.customer,title="Work Completed",message=f"Your booked service has been completed.")
    return redirect(display_providerAcceptedBooking)



@login_required(login_url='/accounts/login')
def provider_cancelledWork(request,bookId):
    booking = Booking.objects.get(id=bookId)
    booking.status="cancelled"
    booking.save()
    Notification.objects.create(receiver=booking.customer,title="Work Cancelled",message=f"Your booked service has been cancelled.")
    return redirect(display_providerAcceptedBooking)




@login_required(login_url='/accounts/login')
def provider_rejectBooking(request,bookId):
    booking = Booking.objects.get(id=bookId)
    # Save old provider as rejected
    booking.rejected_providers.add(booking.provider)
    # Find new provider excluding rejected one.
    available_providers = ServiceProviderProfile.objects.filter(service_field=booking.service.category,
                    is_verified=True,availabilty_status='available').exclude(id__in=booking.rejected_providers.values_list('id',flat=True ))

    if not available_providers.exists():
        booking.status='cancelled'
        booking.save()
        Notification.objects.create(receiver=booking.customer,title="Work Cancelled",message=f"Your booked service has been cancelled.Service provider not available.")
        return redirect(dashboard)
    else:
        # Randomly choose another provider
        new_provider = random.choice(available_providers)

        booking.provider = new_provider
        booking.save()
        return redirect(dashboard)

        

    

    