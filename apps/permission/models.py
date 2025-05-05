from django.db import models
from django.utils.text import slugify

# Create your models here.
# Role - user_types
class Role(models.Model):
    name = models.CharField(max_length=255, default='General')
    slug = models.SlugField(max_length=255, blank=True)
    status = models.CharField(max_length=8, default='1')
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  
        super(Role, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'user_role'
        
class Permission(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    status = models.CharField(max_length=8, default='1')
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    updated_by = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Permission, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'user_permission'
        
class RolePermission(models.Model):
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission_id = models.ForeignKey(Permission, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, default='1')
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    updated_by = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'role_permission'