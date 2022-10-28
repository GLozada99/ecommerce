from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ecommerce.core.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone')
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('phone',),
        }),
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {
            'fields': ('phone',),
        }),
    )
