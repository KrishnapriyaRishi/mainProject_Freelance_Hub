from django.db import models
from services.models import ServiceCategory,Service
from accounts.models import CustomUser,ServiceProviderProfile

# Create your models here.
class Booking(models.Model):
	STATUS_CHOICES = (
		('pending','Pending'),
		('accepted','Accepted'),
		('in_progress','In Progress'),
		('completed','Completed'),
		('cancelled','Cancelled')
	)
	customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='customer_bookings')
	provider = models.ForeignKey(ServiceProviderProfile,on_delete=models.SET_NULL,null=True,blank=True)
	service = models.ForeignKey(Service,on_delete=models.CASCADE)
	scheduled_date = models.DateTimeField(null=True)
	address = models.TextField()
	status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
	rejected_providers = models.ManyToManyField(ServiceProviderProfile,blank=True,related_name='rejected_bookings')
	created_at = models.DateTimeField(auto_now_add=True)
	is_reviewed = models.BooleanField(default=False)
	

	def __str__(self):
		return f"{self.customer.username}-{self.service.name}"
	