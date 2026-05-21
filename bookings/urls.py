from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
path('create_booking/<int:sId>',create_booking,name='create_booking'),
path('provider_acceptBooking/<int:bookId>',provider_acceptBooking,name='provider_acceptBooking'),
path('provider_rejectBooking/<int:bookId>',provider_rejectBooking,name='provider_rejectBooking'),
path('display_providerAcceptedBooking/',display_providerAcceptedBooking,name='display_providerAcceptedBooking'),
path('provider_startWork/<int:bookId>',provider_startWork,name='provider_startWork'),
path('provider_completedWork/<int:bookId>',provider_completedWork,name='provider_completedWork'),
path('provider_cancelledWork/<int:bookId>',provider_cancelledWork,name='provider_cancelledWork'),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)