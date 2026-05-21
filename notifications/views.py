from django.shortcuts import render,redirect
from .models import Notification
from accounts.views import dashboard
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/accounts/login')
def markAsRead(request,noti_Id):
	notif = Notification.objects.get(id=noti_Id)
	notif.is_read=True
	notif.save()
	return redirect(dashboard)
