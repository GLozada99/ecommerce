from ecommerce.products.models import Product
from ecommerce.products.serializers.product import ProductSerializer


class ProductService:

    @staticmethod
    def get_products(
            current_category: str,
            order_by: str
    ) -> list[dict | None]:
        """Returns product list of dicts representation based on
        current_category."""
        products = Product.objects.all()
        if current_category:
            products = products.filter(category__slug=current_category)
        if order_by:
            products = products.order_by(order_by)
        return ProductSerializer(products, many=True).data

    @staticmethod
    def get_order_by_options():
        return [
            {'field_name': 'name', 'show_name': 'Name'},
            {'field_name': 'current_price', 'show_name': 'Price'},
        ]
