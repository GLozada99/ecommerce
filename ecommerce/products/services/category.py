from typing import Sequence

from ecommerce.products.models.models import Category


class CategoryService:

    @staticmethod
    def get_current_category(category_param: str) -> Category:
        return Category.objects.filter(
                slug=category_param
            ).first()

    @staticmethod
    def get_categories() -> Sequence[Category]:
        return Category.objects.all()
