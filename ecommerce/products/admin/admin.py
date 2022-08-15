from django.contrib import admin

from ecommerce.products.admin.inline import ExtraDataInline, ImageProductInline
from ecommerce.products.models import (Category, Product, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'current_price', 'category', 'slug')
    inlines = [ImageProductInline, ExtraDataInline]