from django.db import models


# Create your models here.
class ServiceCategory(models.Model):
	name = models.CharField(max_length=120)
	icon = models.ImageField(upload_to='categories/',null=True,blank=True)
	short_desc = models.CharField(max_length=200,blank=True)

	def __str__(self):
		return self.name
	


class Service(models.Model):
	name = models.CharField(max_length=150)
	desc = models.TextField(null=True,blank=True)
	category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE)
	price = models.IntegerField(null=True)
	is_available = models.BooleanField(default=True)
	
	
	def __str__(self):
		return self.name