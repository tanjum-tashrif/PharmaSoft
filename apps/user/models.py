from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from apps.permission.models import Role
from system.generic.models import BaseModel
from django.utils.text import slugify
from django.db.models import Q

class UserManager(models.Manager):
    def search_by_data(self, search_string):
        return self.get_queryset().filter(
            Q(username__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_no__icontains=search_string) 
        )
    
class User(AbstractBaseUser, BaseModel):
    class UserVerification(models.TextChoices):
        YES = 'yes'
        NO = 'no'

    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=50, blank=True, null=True)
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    user_verification = models.CharField(max_length=8, choices=UserVerification.choices, default=UserVerification.NO)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)
    zip_code = models.CharField(max_length=8, blank=True, null=True)
    status = models.CharField(max_length=8, default='1')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.IntegerField(default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.IntegerField(default=0, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "user"

    objects = UserManager()

    def __str__(self):
        return self.username
    
    @property
    def name(self):
        return self.username

    @property
    def user_role_name(self):
        return self.user_role.name if self.user_role else 'Unknown'
    
    # @property
    # def user_type_name(self):
    #     if self.user_type:
    #         user_type_name = UserTypes.objects.filter(slug=self.user_type).first().name
    #     else:
    #         user_type_name = ''
    #     return user_type_name
        
