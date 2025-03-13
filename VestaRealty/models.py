from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    '''Model for tenants that are registered by the Landlord'''
    landlord = models.ForeignKey(User, related_name='tenants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    unit_number = models.CharField(max_length=20)
    Rent = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.unit_number}"
    
class MonthlyRent(models.Model):
    '''Model to store the monthly rent for the tenants'''
    tenant = models.ForeignKey(Tenant, related_name='rent_records', on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
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

    def __str__(self):
        return f'{self.name} is owned by {self.owned_by}'