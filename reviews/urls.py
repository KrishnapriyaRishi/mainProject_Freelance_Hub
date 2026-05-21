from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
	path('submit_review/<int:booking_id>',submit_review,name='submit_review'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)