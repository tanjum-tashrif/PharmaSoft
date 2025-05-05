from django.db import models
from system.generic.models import BaseModel
from apps.user.models import User
from apps.supplier.models import Supplier
from django.db.models import Q
# Create your models here.

class MedicineManager(models.Manager):
    def search_by_data(self, search_string):
        return self.get_queryset().filter(
            Q(name__icontains=search_string) |
            Q(generic_name__icontains=search_string) |
            Q(batch__icontains=search_string) 
        )

class Medicine(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    generic_name = models.CharField(max_length=255, null=True, blank=True)
    strength = models.CharField(max_length=255, null=True, blank=True)
    shelf = models.CharField(max_length=255, blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)
    # batch = models.CharField(max_length=255, blank=True, null=True)
    # expire_date = models.DateField(null=True, blank=True) 
    # stock = models.PositiveIntegerField(default=0, blank=True, null=True) 
    # price =  models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    supplier_name = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    # supplier_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=8, default='1')
    # box_size = models.ForeignKey('Leaf', on_delete=models.CASCADE, blank=True, null=True)
    # unit = models.ForeignKey('Unit', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    # type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)
    class Meta:
        db_table = 'medicine'

    objects = MedicineManager()

class MedicineBatch(BaseModel):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
    batch = models.CharField(max_length=255)
    expire_date = models.DateField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    box_mrp = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True) # box_mrp
    supplier_name = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    supplier_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    leaf = models.ForeignKey('Leaf', on_delete=models.CASCADE, blank=True, null=True) # Leaf 1 pata = 12 pc
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, blank=True, null=True)  # Box_10 = 10 pata
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True) # Capsule
    status = models.CharField(max_length=8, default='1')
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'medicine_batch'
        # unique_together = ('medicine', 'batch') 

class Category(BaseModel): # Anti Allergic
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=8, default='1')
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)
    class Meta:
        db_table = 'medicine_category'

class Unit(BaseModel): # Box_10 = 10 pata, Pack, Dose
    name = models.CharField(max_length=255, unique=True)
    unit_value = models.PositiveIntegerField(null=True, blank=True) # leaf quantity
    status = models.CharField(max_length=8, default='1')
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)
    class Meta:
        db_table = 'medicine_unit'

class Type(BaseModel): # Capsule
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=8, default='1')
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)
    class Meta:
        db_table = 'medicine_type'

class Leaf(BaseModel): # Leaf 24
    name = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField(null=True, blank=True) # 1 leaf = 12 pc tablet
    status = models.CharField(max_length=8, default='1')
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)
    class Meta:
        db_table = 'medicine_leaf'

