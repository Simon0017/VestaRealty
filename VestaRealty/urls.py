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
    path('rent_info/<int:tenant_id>',views.update_rent_info,name='rent_info'),
    path('view_tenant',views.tenant_info,name='view_tenant'),
    path('create_property',views.create_property,name='create_property'),
    path('view_properties',views.view_properties,name='view_properties'),
    path('view_invoice/<int:invoice_id>',views.view_invoice,name='view_invoice'),
    path('',views.homepage,name=''),
    path('create_invoice',views.create_invoice,name='create_invoice'),
    path('get_rent',views.get_rent,name='get_rent'),
    path('table_invoice',views.view_table_invoice,name='table_invoice'),
    path('update_payments',views.form_update_payment,name = 'update_payments'),
]