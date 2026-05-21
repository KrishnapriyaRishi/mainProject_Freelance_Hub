from django.shortcuts import render,redirect
from .models import Service,ServiceCategory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import addServiceForm

# Create your views here.

def listAllServicesAdmin(request):
	serv = Service.objects.all()
	return render(request,'serviceRelated/listServices_admin.html', {'serv': serv})


def listAllServicesCustomer(request):
	serv = Service.objects.all()
	return render(request,'serviceRelated/listServices_cust.html', {'serv': serv})

def listServicesCategoryBased(request,scId):
	serv = Service.objects.filter(category=scId)
	sc = ServiceCategory.objects.get(id=scId)
	return render(request,'serviceRelated/listServices_category.html', {'serv': serv,'sc':sc})


def addServices(request):
	if request.method == 'POST':
		form = addServiceForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect(listAllServicesAdmin)
	else:

		form = addServiceForm()
	return render(request,'serviceRelated/addServices_admin.html', {'form': form})

def editServiceAdmin(request,sid):
     ser = Service.objects.get(id=sid)
     if request.method == 'POST':
          form = addServiceForm(request.POST,request.FILES,instance=ser)
          if form.is_valid():
               form.save()
               return redirect(listAllServicesAdmin)
     else:
          form = addServiceForm(instance=ser)
     return render(request,'serviceRelated/editServiceForm.html',{'form':form})



def deleteServiceAdmin(request,sid):
     ser = Service.objects.get(id=sid)
     if request.method == 'POST':
          ser.delete()
          return redirect(listAllServicesAdmin)

     return render(request,'serviceRelated/deleteServiceAdmin.html',{'pro':ser})
