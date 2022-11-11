from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString

from ecommerce.order.models.cart import Cart
from ecommerce.order.models.order import Order, OrderProducts


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'cookie_id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'client')


@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_to_order', 'link_to_product', 'quantity',
                    'price')
    search_fields = ('order__id',)

    def link_to_product(self, obj: OrderProducts) -> SafeString:
        link = reverse("admin:products_product_change", args=[obj.product_id])
        return format_html('<a href="{}">{}</a>', link,
                           obj.product)

    link_to_product.short_description = 'Product'  # type: ignore

    def link_to_order(self, obj: OrderProducts) -> SafeString:
        link = reverse("admin:order_order_change", args=[obj.order_id])
        return format_html('<a href="{}">{}</a>', link,
                           obj.order_id)

    link_to_order.short_description = 'Order'  # type: ignore
