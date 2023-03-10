from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from apps.accounts.models import User
# Register your models here.


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ['email', 'first_name', 'last_name',
                    'profile', 'is_staff', 'is_active']
