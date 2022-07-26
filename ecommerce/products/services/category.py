from ecommerce.products.models import Category
from ecommerce.products.serializers.category import (CategorySerializer,
                                                     ShortCategorySerializer, )


class CategoryService:

    @staticmethod
    def get_current_category(category_param: str) -> dict:
        """Returns category dict representation based on category_param."""
        return ShortCategorySerializer(
            Category.objects.filter(
                slug=category_param
            ).first()
        ).data

    @staticmethod
    def get_short_categories() -> list[dict]:
        return ShortCategorySerializer(
            Category.objects.all(), many=True).data

    @staticmethod
    def get_categories() -> list[dict]:
        return CategorySerializer(
            Category.objects.all(), many=True).data
