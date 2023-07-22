from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(AbstractUser):
    username = models.CharField(max_length=255)
    organization_name = models.CharField(max_length=255) # organization name
    email = models.EmailField(null=True, blank=False, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=255,null=True, blank=True)
    profile_pic = models.ImageField(blank=True, upload_to='profile_images/organization/')

    role = models.CharField(max_length=255,default='organization', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','organization_name', 'password']

    def __str__(self):
        return self.organization_name
    

class Employee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=False, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    profile_pic = models.ImageField(blank=True, upload_to='profile_images/employees/')
    dob = models.DateField(null=True, blank=True)

    role = models.CharField(max_length=255,default='employee', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    