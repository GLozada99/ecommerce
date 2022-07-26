from ecommerce.products.models import Product
from ecommerce.products.serializers.product import ProductSerializer


class ProductService:

    @staticmethod
    def get_products(current_category: str) -> list[dict | None]:
        """Returns product list of dicts representation based on
        current_category."""
        products = Product.objects.all()
        if current_category:
            products = products.filter(category__slug=current_category)

        return ProductSerializer(products, many=True).data
