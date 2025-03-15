from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    '''Model for tenants that are registered by the Landlord'''
    landlord = models.ForeignKey(User, related_name='tenants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    id_no = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=15)
    Rent = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    date_joined = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.name} - {self.unit_number}"
    
class MonthlyRent(models.Model):
    '''Model to store the monthly rent for the tenants'''
    tenant = models.ForeignKey(Tenant, related_name='rent_records', on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2,null=True) 
    month = models.DateField()  
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return f"Rent for {self.tenant.name} - {self.month.strftime('%B %Y')}"
    
class Property_Owned(models.Model):
    '''Model to store the properties owned by a Landlord'''
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    owned_by = models.ForeignKey(User, blank=True, null=True,related_name='owner',on_delete=models.CASCADE)
    tenants = models.ManyToManyField(Tenant, blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return f'{self.name} is owned by {self.owned_by}'
    

class invoices(models.Model):
    '''This is a model that stores generates invoices from the landlords'''
    landlord = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='landlord_invoice')
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE,null=True,blank=True,related_name='tenant_invoice')
    rent = models.DecimalField(decimal_places=2,max_digits=10)
    water_bills = models.DecimalField(decimal_places=2,max_digits=10)
    electricity_bills = models.DecimalField(decimal_places=2,max_digits=10)
    balance_carried_down = models.DecimalField(decimal_places=2,max_digits=10)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tenant} of {self.landlord} is invoiced a total of {self.rent + self.water_bills + self.electricity_bills + self.balance_carried_down}'
