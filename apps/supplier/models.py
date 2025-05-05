from django.db import models
from system.generic.models import BaseModel
from apps.user.models import User
from django.db.models import Q
# Create your models here.
class SupplierManager(models.Manager):
    def search_by_data(self, search_string):
        return self.get_queryset().filter(
            Q(name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_no__icontains=search_string) 
        )
class Supplier(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=8, default='1')
    admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)
    
    class Meta:
        db_table = 'supplier'

    objects = SupplierManager()