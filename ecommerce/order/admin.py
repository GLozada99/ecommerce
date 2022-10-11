from django.contrib import admin

from ecommerce.order.models.cart import Cart
from ecommerce.order.models.order import Order


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'cookie_id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['employee', 'client']
