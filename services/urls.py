from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
	path('addServices/',addServices,name='addServices'),
	path('listAllServicesAdmin/',listAllServicesAdmin,name='listAllServicesAdmin'),
	path('editServiceAdmin/<int:sid>',editServiceAdmin,name="editServiceAdmin"),
	path('deleteServiceAdmin/<int:sid>',deleteServiceAdmin,name='deleteServiceAdmin'),
	path('listAllServicesCustomer/',listAllServicesCustomer,name='listAllServicesCustomer'),
	path('listServicesCategoryBased/<int:scId>',listServicesCategoryBased,name='listServicesCategoryBased'),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)