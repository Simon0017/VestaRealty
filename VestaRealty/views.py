from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.utils import timezone
import secrets
import re
from datetime import timedelta


# view for the base.html
def base_view(request):
    return render(request, 'base.html')

# view for user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'status':'success',
                })
        except Exception as e:
            return JsonResponse({
                'status':'error',
            })
    return render(request,'login.html')

# view for user password reset password
def user_reset_password(request):
    return render(request,'forgotPassword.html')


# view for user registration
def user_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            sv = User.objects.create_user(username=username,password=password,email=email)
            sv.first_name = name
            sv.save()

            return JsonResponse({
                'status':'success',
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                'status':'error'
            })
    
    return render(request,'registration.html')

# view for the admin dashboard
def dashboard(request):
    return render(request,'dashboard.html')

# view to create a new tenant
@login_required
def create_tenant(request):
    # retrieve properties owned by the landlord
    landlord = request.user
    properties = list(landlord.owner.all())

    if request.method == 'POST':
        name = request.POST['name']
        id_no = request.POST['id']
        tel = request.POST['tel']
        property_in = request.POST['property']
        date = request.POST['date']
        rent = request.POST['rent']
        notes = request.POST['notes']

        # get the property instance
        property_instance = Property_Owned.objects.get(name = property_in)
        try:
            data = Tenant(
                landlord = landlord,
                name = name,
                id_no = id_no,
                phone_number = tel,
                Rent = rent,
                date_joined = date,
                notes = notes,
                created_at = timezone.now(),
            )

            data.save()

            # add tenant to property
            property_instance.tenants.add(data)

            return JsonResponse({
                'status': 'success',
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'error',
            })

    context = {
        'properties': properties,
    }
    
    return render(request,'createTenant.html',context)

# view to update rent information ie rent paid
def update_rent_info(request):
    return render(request,'updateRecords.html')

# view to view tenant info plus the rental records
def tenant_info(request):
    return render(request,'viewTenant.html')


# view to create a new property
@login_required
def create_property(request):
    # pass the username to the crete property
    user = request.user if request.user.is_authenticated else None
    
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        notes = request.POST['notes']

        try :

            data = Property_Owned(
                name = name,
                location = location,
                owned_by = user,
                notes = notes,
            )

            data.save()

            return JsonResponse({
                'status': 'success',
            })
        except Exception as e :
            print(e)
            return JsonResponse({
                'status': 'error',
            })
        
    context = {
        'user': user,
    }
    return render(request,'createProperty.html',context)

# view to view the properties
def view_properties(request):
    return render(request,'viewProperties.html')

# view for the invoice viewing and download the pdf copy
def view_invoice(request):
    return render(request,'invoice.html')