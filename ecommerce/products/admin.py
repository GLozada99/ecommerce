from django.contrib import admin

from ecommerce.products.models import Category, ImageProduct, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


class ImageProductInline(admin.TabularInline):
    model = ImageProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'current_price', 'category', 'slug')
    inlines = [ImageProductInline]
