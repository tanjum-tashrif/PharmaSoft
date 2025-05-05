from django.db import models
from system.generic.models import BaseModel
from apps.user.models import User
from django.db.models import Q
# Create your models here.

class PaymentManager(models.Manager):
    def search_by_data(self, search_string):
        return self.get_queryset().filter(
            Q(customer_name__icontains=search_string) |
            Q(invoice_number__icontains=search_string) |
            Q(transaction_id__icontains=search_string) 
        )
    
class Payment(BaseModel):
    customer_name = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100) # handcash=1, sslcommerz=2
    transaction_type = models.CharField(max_length=100) # purchase=1, invoice=2
    transaction_id = models.CharField(max_length=255)
    amount_paid = models.IntegerField()
    status = models.CharField(max_length=100)
    admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'payment'

    objects = PaymentManager()
        
class PaymentGateWaySettings(BaseModel):
    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'sslcommerz'