from ecommerce.products.models import Category


class CategoryService:

    @staticmethod
    def get_current_category(category_param: str):
        return Category.objects.filter(
                slug=category_param
            ).first()

    @staticmethod
    def get_categories():
        return Category.objects.all()
