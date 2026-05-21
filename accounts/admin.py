from django.contrib import admin
from .models import CustomUser,CustomerProfile,ServiceProviderProfile
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CustomerProfile)
admin.site.register(ServiceProviderProfile)