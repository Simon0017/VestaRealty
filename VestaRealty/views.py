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
