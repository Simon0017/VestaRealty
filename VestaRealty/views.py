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
    return render(request,'login.html')

# view for user password reset password
def user_reset_password(request):
    return render(request,'forgotPassword.html')


# view for user registration
def user_registration(request):
    return render(request,'registration.html')

# view for the admin dashboard
def dashboard(request):
    return render(request,'dashboard.html')

# view to create a new tenant
def create_tenant(request):
    return render(request,'createTenant.html')

# view to update rent information ie rent paid
def update_rent_info(request):
    return render(request,'updateRecords.html')

# view to view tenant info plus the rental records
def tenant_info(request):
    return render(request,'viewTenant.html')