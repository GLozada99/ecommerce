from typing import Sequence

from django.utils.translation import gettext_lazy as _

from ecommerce.products.models import Product


class ProductService:
    @staticmethod
    def get_products(current_category: str, order_by: str) -> \
            Sequence[Product]:
        products = Product.objects.all()
        if current_category:
            products = products.filter(category__slug=current_category)
        if order_by:
            products = products.order_by(order_by)
        return products

    @staticmethod
    def get_order_by_options() -> list[dict[str, str]]:
        return [
            {'field_name': 'name', 'show_name': _('Name')},
            {'field_name': 'current_price', 'show_name': _('Price')},
        ]
