from django.contrib import admin

from ecommerce.products.models import Product, Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'current_price', 'slug')
