from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from services.models import ServiceCategory

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_approved = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.username
    


class CustomerProfile(models.Model):

    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='customer')
    age = models.IntegerField(null=True)
    location = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class ServiceProviderProfile(models.Model):
    Availability_Choices = (('available','Available'),('busy','Busy'),('offline','Offline'),)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length =120,null=True)
    profile_pic = models.ImageField(upload_to='providers')
    service_field = models.ManyToManyField(ServiceCategory,related_name='providers')
    location = models.CharField(max_length = 100,null=True)
    availabilty_status = models.CharField(max_length=50,choices=Availability_Choices,default='available')
    verification_ID = models.ImageField(upload_to='providerId')
    experience = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    average_rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    
    def service_names(self):
        return ", ".join(
            service.name for service in self.service_field.all()
        )

    def __str__(self):
        return self.user.username
    



