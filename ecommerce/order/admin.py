from django.contrib import admin

from ecommerce.order.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
