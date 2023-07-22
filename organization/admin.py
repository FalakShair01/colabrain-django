from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization

admin.site.register(Organization, UserAdmin)

