from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
	path('markAsRead/<int:noti_Id>',markAsRead,name='markAsRead'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)