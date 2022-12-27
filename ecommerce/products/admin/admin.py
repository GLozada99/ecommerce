from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString

from ecommerce.products.admin.inline import (ConfigurationInline,
                                             ImageInline, )
from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.products.models.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'category', )
    search_fields = ('category__name',)
    inlines = [ImageInline, ConfigurationInline]


@admin.register(ProductConfiguration)
class ProductConfigurationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'link_to_product', 'current_price', 'store_id')

    search_fields = ('product__id', 'store_id')

    def link_to_product(self, obj: ProductConfiguration) -> SafeString:
        link = reverse("admin:products_product_change", args=[obj.product_id])
        return format_html('<a href="{}">{}</a>', link,
                           obj.product)

    link_to_product.short_description = 'Product'  # type: ignore
