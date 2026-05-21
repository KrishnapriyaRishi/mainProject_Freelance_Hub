from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
 path(
        'booking-list/',
        booking_list_view,
        name='booking-list'
    ),

    path(
        'chat/<int:booking_id>/',
        chat_page,
        name='chat-page'
    ),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)