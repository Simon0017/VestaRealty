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
from django.utils.dateparse import parse_date
import secrets
import re
from datetime import timedelta
from .mpesa import *
from django.views.decorators.http import require_http_methods
import logging

# logging
logger = logging.getLogger(__name__)

# view for the base.html
def base_view(request):
    return render(request, 'base.html')

# view for the homepage
def homepage(request):
    return render(request, 'homepage.html')
    # if request.user is not None:
    #     return redirect('dashboard')
    # else:
    #     return redirect('user_login')

# view for user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            if username.endswith('_Ten'):
                username = username[:-4]
                
                # get the tenant
                tenant  = Tenant.objects.get(name  = username)
                if tenant and tenant.password == password:
                    request.session['tenant'] = tenant
                else:
                    return JsonResponse({
                        'status':'error',
                    })
                

            else:
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
@login_required
def dashboard(request):
    # get the list of tenants associated with the landlord
    tenants = list(request.user.tenants.all())

    # get the properties
    properties = list(request.user.owner.all())

    # get the invoices paid record
    paid_inv = []
    tenants_ = list(request.user.tenants.all())
    for tenant in tenants_:
        tenants_paid_inv = list(tenant.paid_tenant.all())
        for inv in tenants_paid_inv:
            paid_inv.append(inv)

     # get the invoices
    all_invoices = list(request.user.landlord_invoice.all().order_by('-created_on'))
    
    # get the unpaid invoices
    unpaid_invoices_ = []
    for invoice in all_invoices:
        check_instance = invoice.paid_invoice.first()
        if not check_instance:
            unpaid_invoices_.append(invoice)

    
    context = {
        'tenants':tenants,
        'properties':properties,
        'payments':paid_inv,
        'unpaid_invoices':unpaid_invoices_,
    }
    return render(request,'dashboard.html',context)

# view for the properties Records 
def property_records(request):
    tenants = list(request.user.tenants.all())

    tenants_information = []
    for tenant in tenants:
        property = tenant.property_owned_set.all().values_list('name',flat  = True)
        property = property[0]
        balances = 0
        balance = list(tenant.tenant_invoice.all())
        '''Logic : if check the invoices if there exixt paid invoices if there is one chck for the balance in th epaid invoice 
        if not take the invoice balaance'''
        for bal in balance:  #bal here stands for the invoice instance
            paid_invoice_instance = bal.paid_invoice.all().first()
            if paid_invoice_instance is not None:
                balances = balances + paid_invoice_instance.balance_carried_down
            else:
                bal_c_d = bal.balance_carried_down if bal.balance_carried_down else 0
                amt = bal.rent + bal.water_bills + bal.electricity_bills + bal_c_d 
                balances = balances + amt
        tenants_information.append({
            'id':tenant.id,
            'name':tenant.name,
            'property':property,
            'balance':balances

        })

    
    # get the properties
    properties = list(request.user.owner.all())

    modified_property  = []
    for property in properties:
        tenants = list(property.tenants.all().values_list('name', flat=True))
        prop_balance = 0
        # search for the tenant in the tenant info list
        for tenant_in in tenants_information:
            if tenant_in['name'] in tenants:
                prop_balance = prop_balance + tenant_in['balance']
        modified_property.append({
            'name': property.name,
            'location': property.location,
            'tenants': len(tenants),
            "balances":prop_balance,
        })

    # get the balance
    total_balance = 0
    for bal in modified_property:
        total_balance = total_balance + bal['balances']
    
    # context
    context = {
        'properties':modified_property,
        'total':total_balance,
    }
    return render(request,'properties_records.html',context)

# view for the tenants records
def tenants_records(request):
    
    tenants = list(request.user.tenants.all())

    tenants_information = []
    for tenant in tenants:
        property = tenant.property_owned_set.all().values_list('name',flat  = True)
        property = property[0]
        balances = 0
        balance = list(tenant.tenant_invoice.all())
        '''Logic : if check the invoices if there exixt paid invoices if there is one chck for the balance in th epaid invoice 
        if not take the invoice balaance'''
        for bal in balance:  #bal here stands for the invoice instance
            paid_invoice_instance = bal.paid_invoice.all().first()
            if paid_invoice_instance is not None:
                balances = balances + paid_invoice_instance.balance_carried_down
            else:
                bal_c_d = bal.balance_carried_down if bal.balance_carried_down else 0
                amt = bal.rent + bal.water_bills + bal.electricity_bills + bal_c_d 
                balances = balances + amt
        tenants_information.append({
            'id':tenant.id,
            'name':tenant.name,
            'property':property,
            'balance':balances

        })

    # context
    context = {
        'tenants':tenants_information
    }
    return render(request,'tenants_records.html',context)

# view for the paid Invoices
def paidInvoices(request):
    # get the invoices paid record
    paid_inv = []
    tenants_ = list(request.user.tenants.all())
    for tenant in tenants_:
        tenants_paid_inv = list(tenant.paid_tenant.all())
        for inv in tenants_paid_inv:
            paid_inv.append(inv)

    context = {
        'payments':paid_inv
    }
    return render(request,'paid_invoices.html',context)

# view for the unpaid invoices
def unpaid_invoices(request):
    # get the invoices
    all_invoices = list(request.user.landlord_invoice.all().order_by('-created_on'))
    
    # get the unpaid invoices
    unpaid_invoices_ = []
    for invoice in all_invoices:
        check_instance = invoice.paid_invoice.first()
        if not check_instance:
            unpaid_invoices_.append(invoice)

    context = {
        'unpaid_invoices':unpaid_invoices_,
    }

    return render(request,'unpaid_invoices.html',context)

# view for the payment records
def payment_records(request):
    # get the invoices paid record
    paid_inv = []
    tenants_ = list(request.user.tenants.all())
    for tenant in tenants_:
        tenants_paid_inv = list(tenant.paid_tenant.all())
        for inv in tenants_paid_inv:
            paid_inv.append(inv)

    return render(request,'payment_records.html',{'payments':paid_inv})

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

# view to update rent information ie PAYMENTS
@login_required
def update_rent_info(request,invoice_id):
    # get the invoice
    invoice = invoices.objects.get(pk = invoice_id)
    
    # get tenant info
    tenant = invoice.tenant

    # get the remaining balance
    rent_history = []
    balances = 0
    balance = list(tenant.tenant_invoice.all())
    '''Logic : if check the invoices if there exixt paid invoices if there is one chck for the balance in th epaid invoice 
    if not take the invoice balaance'''
    for bal in balance:  #bal here stands for the invoice instance
        paid_invoice_instance = bal.paid_invoice.all().first()
        if paid_invoice_instance is not None:
            balances = balances + paid_invoice_instance.balance_carried_down
            rent_history.append({
                'balance': balances,
                'month':paid_invoice_instance.month,
            })
        else:
            bal_c_d = bal.balance_carried_down if bal.balance_carried_down else 0
            amt = bal.rent + bal.water_bills + bal.electricity_bills + bal_c_d 
            balances = balances + amt
            rent_history.append({
                'balance' :balances,
                'month':bal.month,
            })
    # print(rent_history)
    
    context = {
        'tenant': tenant,
        'balance':balances,
        'rent_history':rent_history,
        'invoice':invoice,
    }

    return render(request,'updateRecords.html',context)

# view for the form of the updating the payment
def form_update_payment(request):    
    '''FOR TEH POSTED UPDATE REM TO UPDATE TEH BAL CARRIED DOWN IE THE BALANCE
    MODEL "PAID INVOICE IS USED 
    1.EXTRACT THE INVOICE INSTANCE IE USING THE TENANT AND THE MONTH 
    "'''

    if request.method == 'POST':
        tenant = request.POST['tenant']
        amount = request.POST['amount']
        electricity = request.POST['electricity']
        water = request.POST['water']
        mpesa = request.POST['mpesa']
        notes = request.POST['notes']
        month = request.POST['month']
        
        try:
            # get the tenant instance and the invoice instance for the month
            tenant_instance = Tenant.objects.get(name = tenant)
            invoice_instance  = tenant_instance.tenant_invoice.get(month__icontains = month)
            
            if invoice_instance:
                # calculate the balance
                rent = invoice_instance.rent if invoice_instance.rent is not None else 0
                water_balance = invoice_instance.water_bills if invoice_instance.water_bills is not None else 0
                electricity_balance = invoice_instance.electricity_bills if invoice_instance.electricity_bills is not None else 0
                bal_c_d = invoice_instance.balance_carried_down if invoice_instance.balance_carried_down is not None else 0
                balance = (int(rent)+ int(water_balance) + int(electricity_balance) + (bal_c_d)) - (int(amount) + int(electricity) + int(water))
                
                print(balance)
                payment = paid_invoices(
                    invoice = invoice_instance,
                    tenant  = tenant_instance,
                    rent = amount,
                    water_bills = water,
                    electricity_bills =electricity,
                    mpesa_code = mpesa,
                    month = month,
                    balance_carried_down = balance ,
                    notes = notes
                )

                payment.save()

                return JsonResponse({
                    'status': 'success'
                })

        except Exception as e:
            print(f'Error occurred : {e}')
            return JsonResponse({
                'status':'error'
            })

# view to view tenant info plus the rental records
@login_required
def tenant_info(request):
    landlord = request.user

    # get landlord's tenants
    tenants = list(landlord.tenants.all())
    modified_tenants = []

    for tenant in tenants:
        property = tenant.property_owned_set.all().values_list('name',flat  = True)
        property = property[0]
        balances = 0
        balance = list(tenant.tenant_invoice.all())
        '''Logic : if check the invoices if there exixt paid invoices if there is one chck for the balance in th epaid invoice 
        if not take the invoice balaance'''
        for bal in balance:  #bal here stands for the invoice instance
            paid_invoice_instance = bal.paid_invoice.all().first()
            if paid_invoice_instance is not None:
                balances = balances + paid_invoice_instance.balance_carried_down
            else:
                bal_c_d = bal.balance_carried_down if bal.balance_carried_down else 0
                amt = bal.rent + bal.water_bills + bal.electricity_bills + bal_c_d 
                balances = balances + amt
        modified_tenants.append({
            'name': tenant.name,
            'property': property,
            'id_no': tenant.id_no,
            'balance': balances,
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
@login_required
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
@login_required
def view_invoice(request,invoice_id):
    # retrieve the invoice data
    invoice_data = invoices.objects.get(id = invoice_id)

    bal_c_d = invoice_data.balance_carried_down if invoice_data.balance_carried_down else 0
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
            'total': invoice_data.rent + invoice_data.water_bills + invoice_data.electricity_bills + bal_c_d,
            
        }

    return render(request,'invoice.html',context)

# view for table invoices
@login_required
def view_table_invoice(request):
    # get all the landlords invoice
    invoices_ = list(request.user.landlord_invoice.all())

    # modify invoices
    mod_invoices =[]
    for invoice in invoices_:
        bal_c_d = invoice.balance_carried_down if invoice.balance_carried_down else 0
        mod_invoices.append({
            'id':invoice.id,
            'tenant':invoice.tenant.name,
            'water_bills':invoice.water_bills,
            'electricity_bills':invoice.electricity_bills,
            'balance_carried_down':invoice.balance_carried_down,
            'rent':invoice.rent,
            'month':invoice.month,
            'total': invoice.rent + invoice.water_bills + invoice.electricity_bills + bal_c_d,
            
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

            # REM TO MAKE THE INVOICE UNIQUE IE CHECK IF THERE IS AN INVOICE FOR THE TENANT FOR THAT MONTH
            # IF YES RETURN ERROR IF NOT CREATE AN INVOICE
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
@login_required
@csrf_exempt
def get_rent(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        tenant = Tenant.objects.get(name = data['customer'])
    return JsonResponse({
        'status': 'success',
        'Rent': tenant.Rent,

    })

@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

def checkOut(request):
    if request.method == "POST":
        try:
            phone = '254744239458'  #request.POST.get("phone")  # e.g., 254712345678
            amount = request.POST.get("amount_paying")
            month = request.POST.get('month')
            account_reference = f'Payment to landlord from {phone} for the month {month} amount: {amount}'
            print(account_reference)
            # return JsonResponse({
            #     'status':'success',
            # })

            # callback_url = "http://127.0.0.1:8000/mpesa_callback"
            callback_url = "https://9c67-105-160-52-17.ngrok-free.app/mpesa_callback"

            response = stk_push(phone, amount, account_reference, callback_url,'174379')
            print(response)
            return JsonResponse(response,safe=False)
        except Exception as e:
            logger.error(e)
     
    return render(request,'checkout_payment.html')


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    print("M-Pesa Callback:", data)  # Log response for debugging
    return JsonResponse({"message": "Callback received"}, status=200)

# func to mpesa callback url validation
@csrf_exempt
def mpesa_validation(request):
    data = json.loads(request.body)
    print("Validation Request:", data)  # Debugging
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})  # Accepts transaction


# func to mpesa callback url vconfirmation
@csrf_exempt
def mpesa_confirmation(request):
    data = json.loads(request.body)
    print("Confirmation Request:", data)  # Debugging
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Received"})  # Confirms transaction


# view for the credentials default to share for the tenant login
def tenant_credentials(request,tenant_id):
    tenant = Tenant.objects.get(pk = tenant_id)
    context  = {
        'tenant':tenant,
    }
    return render(request,'tenant_info.html',context)

# view for the delete tenant
@require_http_methods(['DELETE'])
@csrf_exempt
def delete_tenant(request,tenant_id):
    print('request received')
    try:
        tenant  = Tenant.objects.get(id_no = tenant_id)
        tenant.delete()
        return JsonResponse({
            'status':'success',
        },status = 200)
    except Tenant.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Tenant not found'}, status=404)
    except Exception as e:
        print('Error: ',e)
        logger.error('Error: ',e)
        return JsonResponse({
            'status':'error',
            'message':str(e),
        },status = 500)