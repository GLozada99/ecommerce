from ecommerce.products.models import Product


# type: ignore


class ProductService:
    @staticmethod
    def get_products(current_category: str, order_by: str):
        products = Product.objects.all()
        if current_category:
            products = products.filter(category__slug=current_category)
        if order_by:
            products = products.order_by(order_by)
        return products

    @staticmethod
    def get_order_by_options():
        return [
            {'field_name': 'name', 'show_name': 'Name'},
            {'field_name': 'current_price', 'show_name': 'Price'},
        ]
