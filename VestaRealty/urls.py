from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('base',views.base_view,name='base'),
    path('login',views.user_login,name='login'),
    path('registration',views.user_registration,name='registration'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('create_tenant',views.create_tenant,name='create_tenant'),
    path('forgot_password',views.user_reset_password,name='forgot_password'),
    path('rent_info',views.update_rent_info,name='rent_info'),
    path('view_tenant',views.tenant_info,name='view_tenant'),
]