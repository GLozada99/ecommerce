from django.db.models import QuerySet

from ecommerce.products.models.models import Category


class CategoryService:
    @classmethod
    def get_categories(cls) -> QuerySet:
        return Category.objects.all()
