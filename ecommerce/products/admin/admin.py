from django.contrib import admin

from ecommerce.products.admin.inline import (ConfigurationInline,
                                             ImageInline, )
from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.products.models.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'slug')
    inlines = [ImageInline, ConfigurationInline]


@admin.register(ProductConfiguration)
class ProductConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'current_price')
