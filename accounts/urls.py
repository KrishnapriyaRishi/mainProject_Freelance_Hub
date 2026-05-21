from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [

path('',displayHome,name='home'),
path('search_view/',search_view,name='search_view'),
path('login/',loginPage,name='login'),
path('customer_register/',customer_register,name='customer_register'),
path('provider_register/',provider_register,name='provider_register'),
path('logoutPage/',logoutPage,name='logout'),
path('dashboard/',dashboard,name='dashboard'),
path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
path('view_Users/',view_Users,name='view_Users'),
path('view_BookingDetails_Admin/',view_BookingDetails_Admin,name='view_BookingDetails_Admin'),
path('provider_dashboard/',provider_dashboard,name='provider_dashboard'),
path('customer_dashboard/',customer_dashboard,name='customer_dashboard'),
path('customer_profile/',customer_profile,name='customer_profile'),
path('provider_profile/',provider_profile,name='provider_profile'),
path('editCustomerProfile/',editCustomerProfile,name='editCustomerProfile'),
path('editProviderProfile/',editProviderProfile,name='editProviderProfile'),
path('adminApprove_Provider/<int:uid>',adminApprove_Provider,name='adminApprove_Provider'),
path('viewProvider_profile_admin/<int:uid>',viewProvider_profile_admin,name='viewProvider_profile_admin'),
path('listApproved_Providers_Admin/',listApproved_Providers_Admin,name='listApproved_Providers_Admin'),
path('services/',include('services.urls')),
path('bookings/',include('bookings.urls')),
path('reviews/',include('reviews.urls')),
path('chats/',include('chats.urls')),
path('notifications/',include('notifications.urls'))

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)