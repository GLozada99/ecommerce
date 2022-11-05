from django.db.models import QuerySet

from ecommerce.core.models import SlideImage
from ecommerce.products.services.category import CategoryService
from ecommerce.products.services.product import ProductListService


class FrontPageService:

    @staticmethod
    def get_slides(slide_limit: int) -> QuerySet:
        slides = SlideImage.objects.filter(show=True).order_by('order')
        slide_total = slides.count()
        return slides[:min(slide_limit, slide_total)]

    @classmethod
    def get_context(cls, slide_limit: int, product_limit: int) -> dict:
        return {
            'slides': cls.get_slides(slide_limit),
            'products': ProductListService.get_random_products(product_limit),
            'categories': CategoryService.get_categories(),
        }
