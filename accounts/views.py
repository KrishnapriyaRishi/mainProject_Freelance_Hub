from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser,CustomerForm,ProviderForm
from .models import CustomUser,CustomerProfile,ServiceProviderProfile
from services.models import ServiceCategory,Service
from bookings.models import Booking
from reviews.models import Review
from notifications.models import Notification
from django.db.models import Q,Count
import json
from django.db.models.functions import TruncMonth


# Create your views here.
def displayHome(request):
    cat = ServiceCategory.objects.all()
    ser_pro = ServiceProviderProfile.objects.all().order_by('-average_rating')[:3]
    return render(request,'home.html',{'cat':cat,'ser_pro':ser_pro})






def search_view(request):
    query = request.GET.get('q').strip()
    results = []
    
    if query:
        results = Service.objects.filter( Q(category__name__icontains=query)
            | Q(name__icontains=query) 
        )
        
    return render(request, 'home.html', {'results': results, 'query': query})




def customer_register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            customer = form.save()
            CustomerProfile.objects.create(user=customer)
            return redirect(loginPage)
    else:
        form = RegisterUser()
    return render(request, 'accountRelated/registerUser.html', {'form': form})


def provider_register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.role = 'provider'
            pro.save()
            ServiceProviderProfile.objects.create(user=pro)
            return redirect(loginPage)
    else:
        form = RegisterUser()
    return render(request, 'accountRelated/registerUser.html', {'form': form})







def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role=='provider':
                return redirect(dashboard)
            
            return redirect(displayHome)
    return render(request, 'accountRelated/login.html')


def logoutPage(request):
    logout(request)
    return redirect(displayHome)


def dashboard(request):
    if request.user.role == 'customer':
        return redirect(customer_dashboard)
    elif request.user.role == 'provider':
        return redirect(provider_dashboard)
    elif request.user.role == 'admin':
        return redirect(admin_dashboard)
    else:
         return redirect(displayHome)


@login_required(login_url='/accounts/login')
def provider_dashboard(request):
    ser_p = ServiceProviderProfile.objects.get(user=request.user)
    context = {
        
        'total': Booking.objects.filter(provider=ser_p).count(),
        'pending': Booking.objects.filter(provider=ser_p,status='pending').count(),
        'accepted':  Booking.objects.filter(provider=ser_p,status='accepted').count(),
        'completed':  Booking.objects.filter(provider=ser_p,status='completed').count(),
        'booking':Booking.objects.filter(provider=ser_p,status='pending'),
        'review':Review.objects.filter(provider=ser_p).order_by('-created_at')[:5],
    }

    return render(request, 'accountRelated/provider_dashboard.html', context)


@login_required(login_url='/accounts/login')
def customer_dashboard(request):
    
    context = {
        
        'total': Booking.objects.filter(customer=request.user).count(),
        'pending': Booking.objects.filter(customer=request.user,status='pending').count(),
        'completed': Booking.objects.filter(customer=request.user,status='completed').count(),
        'booking':Booking.objects.filter(customer=request.user),
        'notification':Notification.objects.filter(receiver=request.user,is_read=False)
    }

    return render(request, 'accountRelated/customer_dashboard.html', context)


@login_required(login_url='/accounts/login')
def admin_dashboard(request):

    try:
        monthly_bookings = (
            Booking.objects
            .annotate(month=TruncMonth('created_at'))  
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        months_labels = [b['month'].strftime('%B %Y') for b in monthly_bookings if b['month']]
        bookings_counts = [b['count'] for b in monthly_bookings if b['month']]
    except Exception:
        # Fallback empty lists if the date field name fails or database is empty
        months_labels = []
        bookings_counts = []

    context = {
        'users': CustomUser.objects.all().count() or 0,
        'providers': CustomUser.objects.filter(role='provider').count() or 0,
        'customers': CustomUser.objects.filter(role='customer').count() or 0,
        'bookings': Booking.objects.all().count() or 0,
        'completed': Booking.objects.filter(status='completed').count() or 0,
        'pending': Booking.objects.filter(status='pending').count() or 0,
        'services': Service.objects.all().count() or 0,
        'provider_approval':ServiceProviderProfile.objects.filter(is_verified=False),
        'review':Review.objects.all().order_by('-created_at')[:5],
        # Ensure lists default to empty arrays inside json.dumps()
        'months_json': json.dumps(months_labels if months_labels else []),
        'counts_json': json.dumps(bookings_counts if bookings_counts else []),
	
    }
    return render(request, 'accountRelated/admin_dashboard.html', context)


@login_required(login_url='/accounts/login/')
def customer_profile(request):
	cus = CustomerProfile.objects.get(user=request.user)
	return render(request,'accountRelated/customerProfile.html',{'prof':cus})

@login_required(login_url='/accounts/login/')
def provider_profile(request):
	pro = ServiceProviderProfile.objects.get(user=request.user)
	return render(request,'accountRelated/providerProfile.html',{'prof':pro})


@login_required(login_url='/accounts/login/')
def editCustomerProfile(request):
	cus = CustomerProfile.objects.get(user=request.user)
	if request.method == 'POST':
		form = CustomerForm(request.POST,request.FILES,instance=cus)
		if form.is_valid():
			form.save()
			return redirect(customer_profile)
	else:
		form = CustomerForm(instance=cus)
	
	return render(request,'accountRelated/editCustomerProfile.html',{'form':form})




@login_required(login_url='/accounts/login')
def editProviderProfile(request):
	pro = ServiceProviderProfile.objects.get(user=request.user)
	if request.method == 'POST':
		form = ProviderForm(request.POST,request.FILES,instance=pro)
		if form.is_valid():
			form.save()
			return redirect(provider_profile)
	else:
		form = ProviderForm(instance=pro)
	
	return render(request,'accountRelated/editProviderProfile.html',{'form':form})



@login_required(login_url='/accounts/login')
def adminApprove_Provider(request,uid):
     ser = ServiceProviderProfile.objects.get(id=uid)
     ser.is_verified=True
     ser.user.is_approved=True
     ser.save()
     return redirect(admin_dashboard)


@login_required(login_url='/accounts/login')
def viewProvider_profile_admin(request,uid):
	pro = ServiceProviderProfile.objects.get(id=uid)
	return render(request,'accountRelated/providerProfile.html',{'prof':pro})


@login_required(login_url='/accounts/login')
def listApproved_Providers_Admin(request):
     pro = ServiceProviderProfile.objects.filter(is_verified=True)
     return render(request,'accountRelated/listApprovedProviders.html',{'pro':pro})


@login_required(login_url='/accounts/login')
def view_Users(request):
     user = CustomUser.objects.all()
     return render(request,"accountRelated/user_list.html",{'user':user})

@login_required(login_url='/accounts/login')
def view_BookingDetails_Admin(request):
     booking = Booking.objects.all()
     return render(request,"accountRelated/booking_adminView.html",{'booking':booking})