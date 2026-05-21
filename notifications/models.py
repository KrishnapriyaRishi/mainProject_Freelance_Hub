from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Notification(models.Model):
	receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="notifications")
	title = models.CharField(max_length=120)
	message = models.TextField()
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"Notification-{self.receiver.username}"
	