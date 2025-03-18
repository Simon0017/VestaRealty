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

# view for the homepage
def homepage(request):
    if request.user is not None:
        return redirect('dashboard')
    else:
        return redirect('user_login')

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
def update_rent_info(request,tenant_id):
    #get tenant info
    tenant = Tenant.objects.get(id = tenant_id)
    
    context = {
        'tenant': tenant,
    }

    return render(request,'updateRecords.html',context)

# view to view tenant info plus the rental records
def tenant_info(request):
    landlord = request.user

    # get landlord's tenants
    tenants = list(landlord.tenants.all())
    modified_tenants = []

    for tenant in tenants:
        property = tenant.property_owned_set.all().values_list('name',flat  = True)
        property = property[0]
        modified_tenants.append({
            'name': tenant.name,
            'property': property,
            'id_no': tenant.id_no,
            'Rent': tenant.Rent,
            'id': tenant.id,
        })
    
    context = {
        'tenants': modified_tenants,
    }

    return render(request,'viewTenant.html',context)


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
    # get the landlord
    landlord = request.user

    # get the properties
    properties = list(landlord.owner.all())

    modified_property  = []
    for property in properties:
        tenants = list(property.tenants.all().values_list('name', flat=True))
        modified_property.append({
            'name': property.name,
            'location': property.location,
            'tenants': len(tenants),
            'notes': property.notes,
        })
        

    context = {
        'properties': modified_property,
    }

    return render(request,'viewProperties.html',context)

# view for the invoice viewing and download the pdf copy
def view_invoice(request,invoice_id):
    # retrieve the invoice data
    invoice_data = invoices.objects.get(id = invoice_id)

    context = {
            'landlord':request.user.username,
            'email':request.user.email,
            'id':invoice_data.id,
            'tenant':invoice_data.tenant.name,
            'water_bills':invoice_data.water_bills,
            'electricity_bills':invoice_data.electricity_bills,
            'balance_carried_down':invoice_data.balance_carried_down,
            'rent':invoice_data.rent,
            'month':invoice_data.month,
            'total': int(invoice_data.rent) + int(invoice_data.water_bills) + int(invoice_data.electricity_bills),
            
        }

    return render(request,'invoice.html',context)

# view for table invoices
def view_table_invoice(request):
    # get all the landlords invoice
    invoices_ = list(request.user.landlord_invoice.all())

    # modify invoices
    mod_invoices =[]
    for invoice in invoices_:
        mod_invoices.append({
            'id':invoice.id,
            'tenant':invoice.tenant.name,
            'water_bills':invoice.water_bills,
            'electricity_bills':invoice.electricity_bills,
            'balance_carried_down':invoice.balance_carried_down,
            'rent':invoice.rent,
            'month':invoice.month,
            'total': int(invoice.rent) + int(invoice.water_bills) + int(invoice.electricity_bills),
            
        })

    context = {
        'invoices': mod_invoices,
    }
    return render(request,'tableInvoice.html',context)

# view to create the invoices
def create_invoice(request):
    # get the landlords tenants
    landlord = request.user
    tenants = list(landlord.tenants.all())
    if request.method == 'POST':
        customer = request.POST['Customer']
        water = request.POST['water']
        Electricity = request.POST['Electricity']
        month = request.POST['month']

        try:
            # get the user instance
            tenant = Tenant.objects.get(name  = customer)
            data = invoices(
                landlord = landlord,
                tenant = tenant,
                rent = tenant.Rent,
                water_bills = water,
                electricity_bills = Electricity,
                month = month,
            )

            data.save()
            return JsonResponse({
                'status': 'success',
            })
        
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'error',
            })
        
    
    
    context = {
        'tenants': tenants,
    }
    return render(request,'create_invoice.html',context)

# view to get the rent
@csrf_exempt
def get_rent(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        tenant = Tenant.objects.get(name = data['customer'])
    return JsonResponse({
        'status': 'success',
        'Rent': tenant.Rent,

    })